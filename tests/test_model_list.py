from tornado.testing import AsyncTestCase, gen_test

from wormhole.model_list import ModelList
from tests import DatabaseTestCase


class ModelListTestCase(DatabaseTestCase, AsyncTestCase):

    def setUp(self):
        super().setUp()
        self.model_list = ModelList(self.database, self.collection)

    def test_get_default_result(self):
        self.assertIn('result', self.model_list.view)
        self.assertIn('next', self.model_list.view)
        self.assertIn('previous', self.model_list.view)

    @gen_test
    async def test_empty_result(self):
        await self.model_list.find(1)
        self.assertEqual([], self.model_list.view['result'])

    @gen_test
    async def test_previous_with_empty_result(self):
        await self.model_list.find(1)
        self.assertEqual(None, self.model_list.view['previous'])

    @gen_test
    async def test_next_with_empty_result(self):
        await self.model_list.find(1)
        self.assertEqual(None, self.model_list.view['next'])

    @gen_test
    async def test_get_result(self):
        model = self.model_factory()
        await self.model_list.find(1)
        self.assertEqual([model.view], self.model_list.view['result'])

    @gen_test
    async def test_sorted_result(self):
        models = [self.model_factory(), self.model_factory()]
        await self.model_list.find(1)
        self.assertEqual(models[0].view, self.model_list.view['result'][0])
        self.assertEqual(models[1].view, self.model_list.view['result'][1])

    @gen_test
    async def test_default_page(self):
        models = [self.model_factory() for i in range(15)]
        await self.model_list.find(1)
        self.assertEqual(10, len(self.model_list.view['result']))

    @gen_test
    async def test_zero_page(self):
        models = [self.model_factory() for i in range(15)]
        await self.model_list.find(page=0)
        self.assertEqual(10, len(self.model_list.view['result']))

    @gen_test
    async def test_second_page(self):
        models = [self.model_factory() for i in range(15)]
        await self.model_list.find(2)
        self.assertEqual(5, len(self.model_list.view['result']))

    @gen_test
    async def test_show_previous_value(self):
        models = [self.model_factory() for i in range(15)]
        await self.model_list.find(2)
        self.assertEqual(1, self.model_list.view['previous'])

    @gen_test
    async def test_show_next_value(self):
        models = [self.model_factory() for i in range(15)]
        await self.model_list.find(1)
        self.assertEqual(2, self.model_list.view['next'])
