from db._db_interface import *


class CatDBInterface:

    @staticmethod
    def get_cat_by_id(id):
        try:
            db = NoSQLDatabase()
            db.init()
            u = db.find_one_by_key("_id", id, "deck")
        except Exception as ex:
            print("ERROR")
            raise ex
        return u

    @staticmethod
    def update_deck(deck):
        pass


def dev_init():

    print("Initialise cat")
    db = NoSQLDatabase()
    db.init()
    # Cat: id, name, species, description, thumbnail, ability_id,
    test_cat1 = {
        "_id": 1,
        "name": "dummy_cat1",
        "species": "Dummy Species",
        "description": "Mewmewmew",
        "thumbnail": "",
        "ability_id": 1
    }
    test_cat2 = {
        "_id": 2,
        "name": "dummy_cat2",
        "species": "Dummy Species 2",
        "description": "Mewmewmew",
        "thumbnail": "",
        "ability_id": 2
    }
    db.save_record(collection_name="cat", record=test_cat1)
    db.save_record(collection_name="cat", record=test_cat2)
