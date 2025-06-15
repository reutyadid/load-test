from users.base import BaseUser
from connections.factory import get_producer
from locust import task
from data.factory import get_data_handler

class GenericMsgUser(BaseUser):
    def on_start(self):
        tech = self.config["msg_type"]
        self.producer = get_producer(tech, self.config)
        self.data_handler = get_data_handler(self.config.get("data"), self.config.get("json_schema"))

    @task
    def send(self):
        payload = self.data_handler.get_next()
        self.producer.send_message(payload)
 