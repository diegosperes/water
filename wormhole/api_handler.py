from tornado.web import RequestHandler

from wormhole.model import Model
from wormhole.model_list import ModelList
from wormhole import json


class ApiHandler(RequestHandler):
    async def get(self, database, collection, _id):
        if _id:
            view, status_code = await self._get_data(database, collection, _id)
        else:
            view, status_code = await self._get_list(database, collection)

        self.set_status(status_code)
        data = json.dumps(view)
        self.finish(data)

    async def _get_list(self, database, collection):
        model = ModelList(database, collection)
        try:
            page = self.get_argument('page', 1)
            page = int(page)
        except ValueError:
            return model.view, 400

        await model.find(page)
        status_code = 200 if model.has_result() else 404
        return model.view, status_code

    async def _get_data(self, database, collection, _id):
        model = await Model.find(database, collection, _id)
        if model:
            return model.view, 200
        return {}, 404
