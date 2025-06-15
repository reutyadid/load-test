from locust import HttpUser, task

class HTTPUser(HttpUser):
    config = {}

    @task
    def get_endpoint(self):
        self.client.get(self.config.get("endpoint", "/"))