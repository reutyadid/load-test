from abc import ABC, abstractmethod

class BaseDataHandler(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def get_next(self):
        """Return the next data item to send."""
        pass

    def reset(self):
        """Reset data pointer if needed (for repeated tests)."""
        pass