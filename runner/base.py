class RunnerRegistry:
    _registry = {}

    @classmethod
    def register(cls, name):
        def decorator(runner_cls):
            cls._registry[name] = runner_cls
            return runner_cls
        return decorator

    @classmethod
    def get_runner(cls, name):
        runner_cls = cls._registry.get(name)
        if not runner_cls:
            raise ValueError(f"Runner '{name}' is not registered.")
        return runner_cls


class BaseRunner:
    def __init__(self, user_class, shape_class, config):
        self.user_class = user_class
        self.shape_class = shape_class
        self.config = config
    
    def prepare(self, *args, **kwargs):
        pass

    def run(self):
        raise NotImplementedError

    def cleanup(self):
        pass  # Overridden by runners that need cleanup