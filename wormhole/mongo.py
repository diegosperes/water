from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
from tornado.ioloop import IOLoop


executor = ThreadPoolExecutor()
client = MongoClient()


async def run(action, *args, **kwargs):
    loop = IOLoop.current()
    return await loop.run_in_executor(executor, action, *args, **kwargs)


class Mongo:
    def __getattr__(self, action):
        def get_collection(database, collection):
            return client[database][collection]
        async def execute(database, collection, *args, **kwargs):
            _collection = await run(get_collection, database, collection)
            return await run(getattr(_collection, action), *args, **kwargs)
        return execute
