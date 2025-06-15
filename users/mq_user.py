from users.base import BaseUser
import pika
from locust import task

class MQUser(BaseUser):
    def on_start(self):
        mq_conf = self.config["mq"]
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(mq_conf["host"]))
        self.channel = self.connection.channel()

    @task
    def publish(self):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.config["mq"]["queue"],
            body="test"
        )