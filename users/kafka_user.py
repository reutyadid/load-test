from users.base import BaseUser
from kafka import KafkaProducer
from locust import task

class KafkaUser(BaseUser):
    def on_start(self):
        tech = self.config["msg_type"]
        self.producer = get_producer(tech, self.config)

    @task
    def send_message(self):
        payload = "test message"
        self.producer.send_message(payload)