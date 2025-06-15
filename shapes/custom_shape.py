from locust import LoadTestShape

class CustomShape(LoadTestShape):
    def __init__(self, shape_config):
        super().__init__()
        self.shape_config = shape_config
        self.stage = 0

    def tick(self):
        # Example: Use a list of stages [{"users": 10, "spawn_rate": 2, "duration": 60}, ...]
        stages = self.shape_config.get("stages", [])
        if self.stage >= len(stages):
            return None
        stage = stages[self.stage]
        run_time = stage.get("duration", 60)
        if self.get_run_time() > run_time:
            self.stage += 1
            if self.stage >= len(stages):
                return None
            stage = stages[self.stage]
        return (stage.get("users", 1), stage.get("spawn_rate", 1))