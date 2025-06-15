from locust import User

class BaseUser(User):
    abstract = True
    config = {}

    def on_start(self):
        pass

    def on_stop(self):
        pass