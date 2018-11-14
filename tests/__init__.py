import random
from pymongo import MongoClient

from wormhole.model import Model


class DatabaseTestCase:

    def setUp(self):
        super().setUp()
        self.database = 'database'
        self.collection = 'collection'
        self.mongo_client = MongoClient()[self.database][self.collection]

    def tearDown(self):
        self.mongo_client.drop()

    def model_factory(self):
        model = Model(self.database, self.collection, data={'value': random.random()})
        _id = self.mongo_client.insert_one(model.data).inserted_id
        data = self.mongo_client.find_one({'_id': _id})
        return Model(self.database, self.collection, data=data)
