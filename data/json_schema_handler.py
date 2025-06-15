from data.base_handler import BaseDataHandler
from hypothesis_jsonschema import from_schema
import json

class JsonSchemaDataHandler(BaseDataHandler):
    def __init__(self, schema, count=100):
        self.schema = schema
        self.count = count
        self._strategy = from_schema(self.schema)
        self._examples = [self._strategy.example() for _ in range(self.count)]
        self.index = 0

    def get_next(self):
        value = self._examples[self.index % self.count]
        self.index += 1
        return value

    def reset(self):
        self.index = 0