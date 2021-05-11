import json
from datetime import datetime


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            result = obj.__dict__
            return result

        if isinstance(obj, datetime):
            result = obj.strftime("%m/%d/%Y, %H:%M:%S")
            return result

        return {}
