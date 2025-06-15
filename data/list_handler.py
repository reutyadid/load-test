from data.base_handler import BaseDataHandler

class ListDataHandler(BaseDataHandler):
    def __init__(self, data):
        super().__init__(data)
        self.index = 0

    def get_next(self):
        if not self.data:
            return None
        item = self.data[self.index % len(self.data)]
        self.index += 1
        return item

    def reset(self):
        self.index = 0