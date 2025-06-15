from .base import RunnerRegistry

def get_runner(runner_type, user_class, shape_class, config):
    runner_cls = RunnerRegistry.get_runner(runner_type)
    return runner_cls(user_class, shape_class, config)