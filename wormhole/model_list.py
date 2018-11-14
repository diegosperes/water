import pymongo

from wormhole.mongo import Mongo
from wormhole.model import Model


class ModelList:

    client = Mongo()
    LIMIT = 10

    @property
    def view(self):
        return self._result

    def __init__(self, database, collection):
        self.database = database
        self.collection = collection
        self._result = dict(result=[], next=None, previous=None)

    async def find(self, page):
        result = {}
        skip = (page - 1) * self.LIMIT if page > 0 else 0
        self._result['result'] = [self._new_model(data).view for data in await self._paginate(skip)]
        self._result['next'] = await self._set_next(skip, page)
        self._result['previous'] = page - 1 if page > 1 else None

    def has_result(self):
        return bool(self._result['result'])

    def _new_model(self, data):
        return Model(self.database, self.collection, data=data)

    async def _set_next(self, skip, page):
        total = await self.client.count_documents(
                self.database, self.collection, {}, skip=skip, limit=self.LIMIT)
        return page + 1 if total > 0 else None

    async def _paginate(self, skip):
        cursor = await self.client.find(self.database, self.collection)
        return cursor.skip(skip).limit(self.LIMIT)
