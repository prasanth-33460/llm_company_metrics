import json

class JSONFormatter:
    @staticmethod
    def format(data: list) -> str:
        return json.dumps(data, indent=4)