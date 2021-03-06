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
        now = now.replace(microsecond=0) #mongodb does not support microsecond
        self._data.setdefault('created', now)
        self._data.setdefault('updated', now)
        return self._data

    def __init__(self, database, collection, data={}):
        self.database = database
        self.collection = collection
        self._data = data

    async def delete(self):
        await self.client.delete(self.database, self.collection, {'_id': self.data['_id']})

    async def insert(self):
        await self.client.insert(self.database, self.collection, self.data)

    async def update(self, data):
        self.data.update(data)
        query = {'_id': self.data['_id']}
        data = {'$set': self.data}
        await self.client.update(self.database, self.collection, query, data)
