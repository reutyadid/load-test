from connections.base_producer import BaseProducer
import pika

class RabbitMQProducer(BaseProducer):
    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config["host"])
        )
        self.channel = self.connection.channel()

    def send_message(self, message, queue=None):
        queue = queue or self.config["queue"]
        self.channel.basic_publish(exchange='', routing_key=queue, body=message)

    def close(self):
        self.connection.close()