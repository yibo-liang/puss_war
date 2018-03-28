from db._db_interface import *


class CatDBInterface:

    @staticmethod
    def get_cat_by_id(id):
        try:
            db = NoSQLDatabase()
            db.init()
            u = db.find_one_by_key("_id", id, "cat")
        except Exception as ex:
            print("ERROR")
            raise ex
        return u

    @staticmethod
    def get_cats_by_deck_id_list(id_list):
        try:
            db = NoSQLDatabase()
            db.init()
            decks = db.find_all_by_keylist("_id", id_list, "cat")
        except Exception as ex:
            print("Error")
            raise ex
        return decks

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
        "name": "抹茶",
        "species": "",
        "description": "",
        "thumbnail": "002.png",
        "ability_id": 1,
        "health": 50,
    }
    test_cat2 = {
        "_id": 2,
        "name": "圆圆",
        "species": "",
        "description": "",
        "thumbnail": "001.png",
        "ability_id": 2,
        "health": 50,
    }
    db.save_record(collection_name="cat", record=test_cat1)
    db.save_record(collection_name="cat", record=test_cat2)
