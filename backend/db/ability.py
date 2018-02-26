from db._db_interface import *


class AbilityDBInterface:

    @staticmethod
    def get_ability_by_id(id):
        try:
            db = NoSQLDatabase()
            db.init()
            u = db.find_one_by_key("_id", id, "ability")

        except Exception as ex:
            print("ERROR")
            raise ex
        return u

    @staticmethod
    def update_user(user):
        pass


def hash(text="default"):
    return hashlib.sha256(text.encode()).hexdigest()

def dev_init():
    print("Initialise ability")
    db = NoSQLDatabase("puss_war")
    db.init()
    # Ability : id, name, description, leveling(list of list of floats), thumbnail
    test_ability1 = {
        "_id": 1,
        "name": "The world",
        "description": "Stop time, make {} cards free in this round. Cost all acting points",
        "leveling": [[2, 3, 4, 5]],
        "thumbnail": ""
    }
    test_ability2 = {
        "_id": 2,
        "name": "delusional",
        "description": "Randomize the cost of {} cards in your opponents' deck,  Cost must be >= {}.",
        "leveling": [[2, 3, 4, 5], [1, 1, 1, 2]],
        "thumbnail": ""
    }
    db.save_record(collection_name="ability", record=test_ability1)
    db.save_record(collection_name="ability", record=test_ability2)