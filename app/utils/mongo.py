import pymongo
from utils.settings import settings

class Mongo:
    def __init__(self, collection: str):
        self.client = pymongo.MongoClient(settings.mongo_uri)
        self.db = self.client[settings.mongo_db]
        self.collection = self.db[collection]

    def get_collection(self):
        return self.collection

    def close(self):
        self.client.close()

    def find(self, query):
        return list(self.collection.find(query, {"_id": 0}))

    def find_one(self, query):
        return self.collection.find_one(query, {"_id": 0})

    def insert_one(self, document):
        return self.collection.insert_one(document)

    def update_one(self, query, update):
        return self.collection.update_one(query, update)

    def delete_one(self, query):
        return self.collection.delete_one(query)
