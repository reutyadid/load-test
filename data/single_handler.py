from data.base_handler import BaseDataHandler

class SingleDataHandler(BaseDataHandler):
    def get_next(self):
        return self.data