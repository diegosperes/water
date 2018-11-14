import json
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.httpclient import HTTPClientError
from pymongo import MongoClient
from bson.objectid import ObjectId

from wormhole.model import Model
from wormhole.server import make_app
from tests import DatabaseTestCase


class ModelTestCase(DatabaseTestCase, AsyncHTTPTestCase):

    def get_app(self):
        return make_app()

    @gen_test
    async def test_get_data(self):
        model = self.model_factory()
        request = await self.request(model.data['_id'])
        result = json.loads(request.body)

        self.assertEqual(200, request.code)
        self.assertEqual(4, len(result))

    @gen_test
    async def test_get_data_when_does_not_exist(self):
        request = await self.request(ObjectId())
        result = json.loads(request.body)

        self.assertEqual(404, request.code)
        self.assertEqual(0, len(result))

    @gen_test
    async def test_get_data_list_when_does_not_exist(self):
        request = await self.request()
        result = json.loads(request.body)

        self.assertEqual(404, request.code)
        self.assertEqual(3, len(result))
        self.assertEqual(0, len(result['result']))

    @gen_test
    async def test_paginated_data_without_page_value(self):
        [self.model_factory() for i in range(15)]
        request = await self.request()
        result = json.loads(request.body)

        self.assertEqual(200, request.code)
        self.assertEqual(10, len(result['result']))

    @gen_test
    async def test_paginated_data_with_page_value(self):
        [self.model_factory() for i in range(15)]
        request = await self.request('?page=2')
        result = json.loads(request.body)

        self.assertEqual(200, request.code)
        self.assertEqual(5, len(result['result']))

    @gen_test
    async def test_paginated_data_with_wrong_page_value(self):
        [self.model_factory() for i in range(15)]
        request = await self.request('?page=a')
        result = json.loads(request.body)

        self.assertEqual(400, request.code)
        self.assertEqual(0, len(result['result']))

    async def request(self, suffix=''):
        try:
            url = self.get_url('/{0}/{1}/{2}'.format(self.database, self.collection, suffix))
            return await self.http_client.fetch(url)
        except HTTPClientError as error:
            return error.response
