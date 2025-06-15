from connections.kafka_producer import KafkaMessageProducer
from connections.rabbitmq_producer import RabbitMQProducer

PRODUCER_MAP = {
    "kafka": KafkaMessageProducer,
    "rabbitmq": RabbitMQProducer,
    # Add more as needed
}

def get_producer(tech, config):
    producer_cls = PRODUCER_MAP[tech]
    producer = producer_cls(config)
    producer.connect()
    return producer