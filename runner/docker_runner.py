from .base import RunnerRegistry

@RunnerRegistry.register("docker")
class DockerRunner(BaseRunner):
    def __init__(self, user_class, shape_class, config):
        self.user_class = user_class
        self.shape_class = shape_class
        self.config = config

    def run(self):
        # Here you would use docker-py or subprocess to start a Docker container
        print("DockerRunner: Would launch Docker container with config:", self.config)

    def cleanup(self):
            pass