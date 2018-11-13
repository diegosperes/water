from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
from tornado.ioloop import IOLoop


async def run(executor, action, *args, **kwargs):
    loop = IOLoop.current()
    return await loop.run_in_executor(executor, action, *args, **kwargs)


async def get_collection(executor, client, database, collection):
    def get(client, database, collection):
        return client[database][collection]
    return await run(executor, get, client, database, collection)


class Mongo:

    def __init__(self):
        self._executor = ThreadPoolExecutor()
        self._client = MongoClient()

    async def find(self, database, collection, *args, **kwargs):
        def _find(collection, *args, **kwargs):
            return collection.find_one(*args, **kwargs)
        return await self._run(database, collection, _find, *args, **kwargs)

    async def delete(self, database, collection, *args, **kwargs):
        def _delete(collection, *args, **kwargs):
            return collection.delete_one(*args, **kwargs)
        return await self._run(database, collection, _delete, *args, **kwargs)

    async def _run(self, database, collection, action, *args, **kwargs):
        collection = await get_collection(self._executor, self._client, database, collection)
        return await run(self._executor, action, collection, *args, **kwargs)
