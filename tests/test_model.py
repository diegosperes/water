import datetime
from tornado.testing import AsyncTestCase, gen_test
from pymongo import MongoClient

from wormhole.model import Model


class ModelTestCase(AsyncTestCase):

    def setUp(self):
        super().setUp()
        self.database = "database"
        self.collection = "collection"
        self.model = Model(self.database, self.collection)
        self.client = MongoClient()[self.database][self.collection]

    def tearDown(self):
        self.client.drop()

    def test_setup_database(self):
        self.assertEqual(self.database, self.model.database)

    def test_setup_collection(self):
        self.assertEqual(self.collection, self.model.collection)

    def test_setup_created(self):
        self.assertIsInstance(self.model.data['created'], datetime.datetime)

    def test_setup_updated(self):
        self.assertIsInstance(self.model.data['updated'], datetime.datetime)

    def test_should_not_override_created(self):
        created = datetime.datetime.now()
        model = Model(self.database, self.collection, data={'created': created})
        self.assertEqual(created, model.data['created'])

    def test_should_not_override_updated(self):
        updated = datetime.datetime.now()
        model = Model(self.database, self.collection, data={'updated': updated})
        self.assertEqual(updated, model.data['updated'])

    @gen_test
    async def test_find(self):
        _id = self.client.insert_one({}).inserted_id
        model = await Model.find(self.database, self.collection, _id)
        self.assertEqual(_id, model.data['_id'])

    @gen_test
    async def test_insert(self):
        model = Model(self.database, self.collection)
        await model.insert()
        data = self.client.find_one({'_id': model.data['_id']})
        self.assertEqual(data, model.data)

    @gen_test
    async def test_update(self):
        _id = self.client.insert_one({}).inserted_id
        model = Model(self.database, self.collection, data={'_id': _id})
        expected = model.data.copy()
        expected['name'] = 'batman'
        await model.update({'name': 'batman'})
        self.assertEqual(expected, self.client.find_one({'_id': _id}))

    @gen_test
    async def test_delete(self):
        _id = self.client.insert_one({}).inserted_id
        model = Model(self.database, self.collection, data={'_id': _id})
        await model.delete()
        self.assertFalse(self.client.find_one({'_id': _id}))
