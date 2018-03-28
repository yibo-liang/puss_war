from db._db_interface import *
import json


class UserDBInterface:

    @staticmethod
    def get_user_by_id(id):
        try:
            db = NoSQLDatabase()
            db.init()
            u = db.find_one_by_key("_id", id, "user")
            if u is None:
                return None
            return u
        except Exception as ex:
            print("ERROR")
            raise ex

    @staticmethod
    def get_user_by_username(username):
        try:
            db = NoSQLDatabase()
            db.init()
            u = db.find_one_by_key("username", username, "user")
            if u is None:
                return None
            return u
        except Exception as ex:
            print("ERROR")
            raise ex

    @staticmethod
    def update_user(user):
        pass


def hash(text="default"):
    return hashlib.sha256(text.encode()).hexdigest()


def dev_init():
    print("Initialise users")
    db = NoSQLDatabase("puss_war")
    db.init()
    # User : uid, username, password(hash sha256), decks(list of deck_id), cats(list of {cat_id, info}), agent_id
    test_u1 = {
        ""
        "_id": 1,
        "username": "pi@test.com",
        "password": hash("admin"),

        "default_deck": 0,
        "default_cat": 0,
        "decks": [
            1
        ],
        "cats": [
            {
                "cat_id": 1,
                "level": 1,
                "exp": 0
            },
        ],
        "apostle_id": 1
    }
    test_u2 = {
        "_id": 2,
        "username": "pi2@test.com",
        "password": hash("admin"),

        "default_deck": 0,
        "default_cat": 0,
        "decks": [
            2
        ],
        "cats": [
            {
                "cat_id": 2,
                "level": 1,
                "exp": 0
            },
        ],
        "apostle_id": 1
    }
    db.save_record(collection_name="user", record=test_u1)
    db.save_record(collection_name="user", record=test_u2)
