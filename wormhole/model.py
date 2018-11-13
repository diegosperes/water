import datetime

from wormhole.mongo import Mongo


class Model:

    client = Mongo()

    @classmethod
    async def find(cls, database, collection, _id):
        data = await cls.client.find(database, collection, {'_id': _id})
        if data:
            return cls(database, collection, data=data)

    @property
    def data(self):
        now = datetime.datetime.now()
        self._data.setdefault('created', now)
        self._data.setdefault('updated', now)
        return self._data

    def __init__(self, database, collection, data={}):
        self.database = database
        self.collection = collection
        self._data = data

    async def delete(self):
        await self.client.delete(self.database, self.collection, {'_id': self.data['_id']})
