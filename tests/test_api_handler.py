import json
from tornado.testing import AsyncHTTPTestCase, gen_test
from pymongo import MongoClient

from wormhole.model import Model
from wormhole.server import make_app


database = 'database'
collection = 'collection'


class ModelTestCase(AsyncHTTPTestCase):
    
    client = MongoClient()[database][collection]

    def get_app(self):
        return make_app()
    
    def setUp(self):
        super().setUp()
        self.model = Model(database, collection)
        _id = self.client.insert_one(self.model.data).inserted_id
        data = self.client.find_one({'_id': _id})
        self.model = Model(database, collection, data=data)
    
    @gen_test
    async def test_get_data(self):
        request = await self.request(self.model.data['_id'])
        result = json.loads(request.body)

        self.assertEqual(200, request.code)
        self.assertEqual(3, len(result))

    async def request(self, suffix):
        url = self.get_url('/{0}/{1}/{2}'.format(database, collection, suffix))
        return await self.http_client.fetch(url)
