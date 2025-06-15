from connections.base_producer import BaseProducer
from kafka import KafkaProducer

class KafkaMessageProducer(BaseProducer):
    def connect(self):
        self.producer = KafkaProducer(
            bootstrap_servers=self.config["bootstrap_servers"]
        )

    def send_message(self, message, topic=None):
        topic = topic or self.config["topic"]
        self.producer.send(topic, message.encode("utf-8"))

    def close(self):
        self.producer.close()