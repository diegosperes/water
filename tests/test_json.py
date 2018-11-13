import datetime
from tornado.testing import AsyncTestCase
from bson.objectid import ObjectId

from wormhole import json


class JsonEncoderTestCase(AsyncTestCase):

    def test_encode_object_id(self):
        data = {'id': ObjectId('5beaf78d08301f452d55b0bd')}
        self.assertEqual('{"id": "5beaf78d08301f452d55b0bd"}', json.dumps(data))

    def test_encode_datetime(self):
        date = datetime.datetime(2018, 11, 13, 15, 6, 30)
        self.assertEqual('{"created": "2018-11-13T15:06:30"}', json.dumps({'created': date}))
