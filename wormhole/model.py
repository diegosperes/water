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
    def query(self):
        return {'_id': self.data['_id']}

    @property
    def data(self):
        now = datetime.datetime.now().replace(microsecond=0) #mongodb does not support microsecond
        self._data.setdefault('created', now)
        self._data.setdefault('updated', now)
        return self._data

    @property
    def view(self):
        view = self.data.copy()
        view['id'] = str(self.data['_id'])
        del view['_id']
        return view

    def __init__(self, database, collection, data={}):
        self.database = database
        self.collection = collection
        self._data = data

    async def delete(self):
        await self.client.delete(self.database, self.collection, self.query)

    async def insert(self):
        await self.client.insert(self.database, self.collection, self.data)

    async def update(self, data):
        self.data.update(data)
        data = {'$set': self.data}
        await self.client.update(self.database, self.collection, self.query, data)
