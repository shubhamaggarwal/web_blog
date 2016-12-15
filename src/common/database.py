import pymongo


class Database(object):
    URI='mongodb://127.0.0.1:27017'
    DATABASE=None

    @staticmethod
    def initialize():
        Database.client=pymongo.MongoClient(Database.URI)
        Database.DATABASE=Database.client['fullstack']

    @staticmethod
    def insert(collection,data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find_one(collection,data):
        data=Database.DATABASE[collection].find_one(data)
        return data

    @staticmethod
    def find_all(collection,data):
        data=Database.DATABASE[collection].find(data)
        return data