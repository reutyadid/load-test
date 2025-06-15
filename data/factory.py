from data.list_handler import ListDataHandler
from data.single_handler import SingleDataHandler
from data.json_schema_handler import JsonSchemaDataHandler

def get_data_handler(data, json_schema=None, count=100):
    if json_schema:
        return JsonSchemaDataHandler(json_schema, count)
    elif isinstance(data, list):
        return ListDataHandler(data)
    else:
        return SingleDataHandler(data)