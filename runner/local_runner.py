from .base import RunnerRegistry
from locust.env import Environment
from locust.stats import stats_printer, stats_history
import gevent

@RunnerRegistry.register("local")
class LocalRunner(BaseRunner):
    def __init__(self, user_class, shape_class, config):
        self.user_class = user_class
        self.shape_class = shape_class
        self.config = config

    def run(self):
        env = Environment(user_classes=[self.user_class], shape_class=self.shape_class)
        env.create_local_runner()
        gevent.spawn(stats_printer(env.stats))
        gevent.spawn(stats_history, env.runner)
        env.runner.start(**self.config.get("runner", {"user_count": 1, "spawn_rate": 1}))
        gevent.spawn_later(self.config.get("run_time", 60), lambda: env.runner.quit())
        env.runner.greenlet.join()

    def cleanup(self):
            pass