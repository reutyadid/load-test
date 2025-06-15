import os
from kubernetes import client, config as k8s_config
from .base import BaseRunner, RunnerRegistry
from utils.image_builder import build_and_push_image

@RunnerRegistry.register("openshift")
class OpenshiftRunner(BaseRunner):
    def __init__(self, user_class, shape_class, config):
        self.user_class = user_class
        self.shape_class = shape_class
        self.config = config
        self.namespace = config.get("k8s_namespace", "default")
        self.image = config.get("image")
        self.job_name = config.get("job_name", f"loadtest-{os.urandom(4).hex()}")
        self.env = config.get("env", {})
        self.command = config.get("command")
        self.resources = config.get("resources", {})
        self.backoff_limit = config.get("backoff_limit", 0)
        self.image_pull_secret = config.get("image_pull_secret")
        self.k8s_context = config.get("k8s_context")

    def prepare(self, locustfile_contents=None, requirements=None, registry_url=None):
        # Only build image if not already set
        if not self.config.get("image"):
            image_name = build_and_push_image(
                base_image="python:3.11-slim",
                locustfile_contents=locustfile_contents,
                requirements=requirements,
                registry_url=registry_url
            )
            self.config["image"] = image_name
            self.image = image_name

    def run(self):
        # Always use the latest image from config
        self.image = self.config.get("image", self.image)
        # Load kube config
        if "KUBERNETES_SERVICE_HOST" in os.environ:
            k8s_config.load_incluster_config()
        else:
            k8s_config.load_kube_config(context=self.k8s_context)

        batch_v1 = client.BatchV1Api()

        # Prepare env vars
        env_vars = [client.V1EnvVar(name=k, value=str(v)) for k, v in self.env.items()]

        # Prepare resources
        resource_requirements = None
        if self.resources:
            resource_requirements = client.V1ResourceRequirements(
                limits=self.resources.get("limits"),
                requests=self.resources.get("requests")
            )

        # Image pull secrets
        image_pull_secrets = None
        if self.image_pull_secret:
            image_pull_secrets = [client.V1LocalObjectReference(name=self.image_pull_secret)]

        # Container
        container = client.V1Container(
            name="loadtest",
            image=self.image,
            env=env_vars,
            resources=resource_requirements,
            command=self.command
        )

        # Pod template
        pod_spec_kwargs = {
            "restart_policy": "Never",
            "containers": [container],
        }
        if image_pull_secrets:
            pod_spec_kwargs["image_pull_secrets"] = image_pull_secrets

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"job-name": self.job_name}),
            spec=client.V1PodSpec(**pod_spec_kwargs)
        )

        # Job spec
        job_spec = client.V1JobSpec(
            template=template,
            backoff_limit=self.backoff_limit
        )

        # Job object
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=self.job_name),
            spec=job_spec
        )

        # Launch the Job
        print(f"OpenshiftRunner: Creating job {self.job_name} in namespace {self.namespace}")
        batch_v1.create_namespaced_job(
            body=job,
            namespace=self.namespace
        )
        print(f"OpenshiftRunner: Job {self.job_name} created")

    def cleanup(self):
        if not self.job_name:
            print("OpenshiftRunner: No job to clean up")
            return

        if "KUBERNETES_SERVICE_HOST" in os.environ:
            k8s_config.load_incluster_config()
        else:
            k8s_config.load_kube_config(context=self.k8s_context)

        batch_v1 = client.BatchV1Api()
        print(f"OpenshiftRunner: Deleting job {self.job_name} in namespace {self.namespace}")
        try:
            batch_v1.delete_namespaced_job(
                name=self.job_name,
                namespace=self.namespace,
                body=client.V1DeleteOptions(
                    propagation_policy="Foreground"
                )
            )
            print(f"OpenshiftRunner: Job {self.job_name} deleted")
        except Exception as e:
            print(f"OpenshiftRunner: Error deleting job: {e}")