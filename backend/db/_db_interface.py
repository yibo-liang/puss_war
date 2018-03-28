import hashlib
from pymongo import MongoClient
import config


def hash(text="default"):
    return hashlib.sha256(text.encode()).hexdigest()


class NoSQLDatabase:
    def __init__(self, db_name=None):
        self.HOST = config.DB_HOST
        self.PORT = config.DB_PORT

        if db_name is None:
            self.DB_NAME = config.DB_NAME
        else:
            self.DB_NAME = db_name

        self.client = None
        self.db = None

    def init(self):
        self.client = MongoClient(self.HOST, self.PORT)
        self.db = self.client[self.DB_NAME]

    # save record to collection, ignore whatever
    def save_record(self, collection_name, record):
        # print(record)
        collection = self.db[collection_name]
        collection.insert_one(record)
        return True

    # update an existing record
    def update_record(self, _id, collection_name, update_info):
        # if the record does not exist raise error
        # update info in form {"key_name":value , "key_name2":value, ...}

        collection = self.db[collection_name]
        collection.update({'_id': _id}, {"$set": update_info}, upsert=False)
        # otherwise update

    def upsert_record(self, _id, collection_name, update_info):
        # if the record does not exist raise error
        # update info in form {"key_name":value , "key_name2":value, ...}

        collection = self.db[collection_name]
        collection.update({'_id': _id}, {"$set": update_info}, upsert=True)
        # otherwise update

    # given key and collection name, return the doc, if not found return None
    def find_one_by_key(self, key_name, value, collection_name):
        collection = self.db[collection_name]
        result = collection.find({key_name: value})

        if result.count() == 1:
            return result[0]
        elif result.count() > 1:
            print("Attempt to find one record for key = %d, val = %d" % (key_name, value))
            raise Exception("Error finding records in db.")
        elif result.count() == 0:
            return None

    def find_all_by_keylist(self, key_name, val_list, collection_name):
        collection = self.db[collection_name]
        result = collection.find({key_name: {"$in": val_list}})
        docs = []
        for doc in result:
            docs.append(doc)
        return docs

    def find_all_by_key(self, key_name, value, collection_name, limit=99999):
        collection = self.db[collection_name]
        result = collection.find({key_name: value})
        docs = []
        count = 0
        for doc in result:
            if count > limit:
                break
            docs.append(doc)
            count += 1
        return docs

    def for_each_record(self, func):
        i = 0
        for document in self.collection.find():
            func(document)
            i += 1
            print("Doc i = %d" % i)

    def empty_db(self):
        self.client.drop_database("puss_war")
