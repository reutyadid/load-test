import os
import uuid
from kubernetes import client, config as k8s_config
from .base import BaseRunner, RunnerRegistry

@RunnerRegistry.register("k8s")
class K8sRunner(BaseRunner):
    def __init__(self, user_class, shape_class, config):
        self.user_class = user_class
        self.shape_class = shape_class
        self.config = config
        self.namespace = config.get("k8s_namespace", "default")
        self.image = config["image"]  # Must be provided in config!
        self.job_name = config.get("job_name", f"loadtest-{uuid.uuid4().hex[:8]}")
        self.env = config.get("env", {})
        self.command = config.get("command", None)
        self.resources = config.get("resources", {})
        self.backoff_limit = config.get("backoff_limit", 0)
        self.k8s_context = config.get("k8s_context", None)  # Optional
        
    def run(self):
        # Load kube config (in-cluster or from file)
        if "KUBERNETES_SERVICE_HOST" in os.environ:
            k8s_config.load_incluster_config()
        else:
            k8s_config.load_kube_config(context=self.k8s_context)

        batch_v1 = client.BatchV1Api()

        # Prepare environment variables
        env_vars = [client.V1EnvVar(name=k, value=str(v)) for k, v in self.env.items()]

        # Prepare resource requirements
        resource_requirements = None
        if self.resources:
            resource_requirements = client.V1ResourceRequirements(
                limits=self.resources.get("limits"),
                requests=self.resources.get("requests")
            )

        # Prepare the container
        container = client.V1Container(
            name="loadtest",
            image=self.image,
            env=env_vars,
            resources=resource_requirements,
            command=self.command
        )

        # Pod template spec
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"job-name": self.job_name}),
            spec=client.V1PodSpec(
                restart_policy="Never",
                containers=[container]
            )
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
        print(f"K8sRunner: Creating job {self.job_name} in namespace {self.namespace}")
        batch_v1.create_namespaced_job(
            body=job,
            namespace=self.namespace
        )
        print(f"K8sRunner: Job {self.job_name} created")

    def cleanup(self):
        # Delete the Job and pods
        if not hasattr(self, "job_name"):
            print("K8sRunner: No job to clean up")
            return

        if "KUBERNETES_SERVICE_HOST" in os.environ:
            k8s_config.load_incluster_config()
        else:
            k8s_config.load_kube_config(context=self.k8s_context)

        batch_v1 = client.BatchV1Api()
        core_v1 = client.CoreV1Api()

        print(f"K8sRunner: Deleting job {self.job_name} in namespace {self.namespace}")
        try:
            batch_v1.delete_namespaced_job(
                name=self.job_name,
                namespace=self.namespace,
                body=client.V1DeleteOptions(
                    propagation_policy="Foreground"
                )
            )
            print(f"K8sRunner: Job {self.job_name} deleted")
        except Exception as e:
            print(f"K8sRunner: Error deleting job: {e}")

        # Optionally, delete pods with label job-name=self.job_name
        try:
            pods = core_v1.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f"job-name={self.job_name}"
            )
            for pod in pods.items:
                core_v1.delete_namespaced_pod(
                    name=pod.metadata.name,
                    namespace=self.namespace,
                    body=client.V1DeleteOptions()
                )
            print(f"K8sRunner: Related pods deleted")
        except Exception as e:
            print(f"K8sRunner: Error deleting pods: {e}")