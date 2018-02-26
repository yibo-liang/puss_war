from db._db_interface import *


class ApostleDBInterface:

    @staticmethod
    def get_apostle_by_id(id):
        try:
            db = NoSQLDatabase()
            db.init()
            u = db.find_one_by_key("_id", id, "deck")
        except Exception as ex:
            print("ERROR")
            raise ex
        return u

    @staticmethod
    def update_apostle(deck):
        pass


def dev_init():
    # Agent : id, name, thumbnail

    print("Initialise apostle")
    db = NoSQLDatabase()
    db.init()
    test_agent1 = {
        "_id": 1,
        "name": "Xiaoming",
        "thumbnail": ""
    }
    test_agent2 = {
        "_id": 2,
        "name": "Xiaohong",
        "thumbnail": ""
    }
    db.save_record(collection_name="apostle", record=test_agent1)
    db.save_record(collection_name="apostle", record=test_agent2)
