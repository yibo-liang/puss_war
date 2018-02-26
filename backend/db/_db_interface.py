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


# Database design Draft 1
# User : uid, username, password(hash sha256), decks(list of deck_id), cats(list of {cat_id, info}), agent_id
# Deck : id, title, cards(list of obj{card_id, info})
# Card : id, title, description, thumbnail
# Cat : id, name, species, description, thumbnail, ability_id,
# Agent : id, name, thumbnail
# Ability : id, name, description, leveling(list of list of floats), thumbnail

# def project_db_init():
    # execute only if run as a script
    # print("Initialise Database")
    # db = NoSQLDatabase("puss_war")
    # db.init()
    # db.empty_db()

    # User : uid, username, password(hash sha256), decks(list of deck_id), cats(list of {cat_id, info}), agent_id
    # test_u1 = {
    #     ""
    #     "_id": 1,
    #     "username": "pi@test.com",
    #     "password": hash("admin"),
    #     "decks": [
    #         1
    #     ],
    #     "cats": [
    #         {
    #             "cat_id": 1,
    #             "level": 1,
    #             "exp": 0
    #         },
    #     ],
    #     "agent_id": 1
    # }
    # test_u2 = {
    #     "_id": 2,
    #     "username": "pi2@test.com",
    #     "password": hash("admin"),
    #     "decks": [
    #         2
    #     ],
    #     "cats": [
    #         {
    #             "cat_id": 1,
    #             "level": 1,
    #             "exp": 0
    #         },
    #     ],
    #     "agent_id": 1
    # }
    # db.save_record(collection_name="user", record=test_u1)
    # db.save_record(collection_name="user", record=test_u2)


    # # Card : id, title, description, thumbnail
    # test_card1 = {
    #     "_id": 1,
    #     "title": "attack",
    #     "description": "Human Attack once",
    #     "thumbnail": ""
    # }
    # test_card2 = {
    #     "_id": 2,
    #     "title": "dodge",
    #     "description": "Avoid next attack within 2 rounds",
    #     "thumbnail": ""
    # }
    # db.save_record(collection_name="card", record=test_card1)
    # db.save_record(collection_name="card", record=test_card2)

    # Cat : id, name, species, description, thumbnail, ability_id,
    # test_cat1 = {
    #     "_id": 1,
    #     "name": "dummy_cat1",
    #     "species": "Dummy Species",
    #     "description": "Mewmewmew",
    #     "thumbnail": "",
    #     "ability_id": 1
    # }
    # test_cat2 = {
    #     "_id": 2,
    #     "name": "dummy_cat2",
    #     "species": "Dummy Species 2",
    #     "description": "Mewmewmew",
    #     "thumbnail": "",
    #     "ability_id": 2
    # }
    # db.save_record(collection_name="cat", record=test_cat1)
    # db.save_record(collection_name="cat", record=test_cat2)

    # Agent : id, name, thumbnail
    # test_agent1 = {
    #     "_id": 1,
    #     "name": "Xiaoming",
    #     "thumbnail": ""
    # }
    # test_agent2 = {
    #     "_id": 2,
    #     "name": "Xiaoming",
    #     "thumbnail": ""
    # }
    # db.save_record(collection_name="agent", record=test_agent1)
    # db.save_record(collection_name="agent", record=test_agent2)
    #
    # # Ability : id, name, description, leveling(list of list of floats), thumbnail
    # test_ability1 = {
    #     "_id": 1,
    #     "name": "The world",
    #     "description": "Stop time, make %d cards free in this round. Cost all acting points",
    #     "leveling": [[2, 3, 4, 5]],
    #     "thumbnail": ""
    # }
    # test_ability2 = {
    #     "_id": 2,
    #     "name": "delusional",
    #     "description": "Randomize the cost of %d cards in your opponents' deck,  Cost must be >= %d.",
    #     "leveling": [[2, 3, 4, 5], [1, 1, 1, 2]],
    #     "thumbnail": ""
    # }
    # db.save_record(collection_name="ability", record=test_ability1)
    # db.save_record(collection_name="ability", record=test_ability2)

