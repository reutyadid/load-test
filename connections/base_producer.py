from abc import ABC, abstractmethod

class BaseProducer(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send_message(self, message, **kwargs):
        pass

    @abstractmethod
    def close(self):
        pass