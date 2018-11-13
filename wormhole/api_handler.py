from tornado.web import RequestHandler

from wormhole.model import Model
from wormhole import json


class ApiHandler(RequestHandler):
    async def get(self, database, collection, _id):
        model = await Model.find(database, collection, _id)
        self.finish(json.dumps(model.view))
