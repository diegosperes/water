import json
import datetime
from bson.objectid import ObjectId


def dumps(data):
    return json.dumps(data, cls=JsonEncoder)


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(self, obj)
