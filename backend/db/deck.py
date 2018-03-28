from db._db_interface import *


class DeckDBInterface:

    @staticmethod
    def get_deck_by_id(id):
        try:
            db = NoSQLDatabase()
            db.init()
            deck = db.find_one_by_key("_id", id, "deck")
        except Exception as ex:
            print("ERROR")
            raise ex
        return deck

    @staticmethod
    def get_decks_by_deck_id_list(id_list):
        try:
            db = NoSQLDatabase()
            db.init()
            decks = db.find_all_by_keylist("_id", id_list, "deck")
        except Exception as ex:
            print("Error")
            raise ex
        return decks

    @staticmethod
    def update_deck(deck):
        pass


def dev_init():
    # Deck : id, title, cards(list of obj{card_id, info})

    print("Initialise deck")
    db = NoSQLDatabase()
    db.init()
    test_deck1 = {
        "_id": 1,
        "title": "test_deck",
        "apostle_cards": [
            {"card_id": 1},
            {"card_id": 1},
            {"card_id": 1},
            {"card_id": 2},
            {"card_id": 2},
            {"card_id": 2},
        ],
        "cat_cards": [
            {"card_id": 10001},
            {"card_id": 10001},
            {"card_id": 10001},
            {"card_id": 10002},
            {"card_id": 10002},
            {"card_id": 10002},
        ]
    }
    test_deck2 = {
        "_id": 2,
        "title": "test_deck",
        "apostle_cards": [
            {"card_id": 1},
            {"card_id": 1},
            {"card_id": 1},
            {"card_id": 2},
            {"card_id": 2},
            {"card_id": 2},
        ],
        "cat_cards": [
            {"card_id": 10001},
            {"card_id": 10001},
            {"card_id": 10001},
            {"card_id": 10002},
            {"card_id": 10002},
            {"card_id": 10002},
        ]
    }
    db.save_record(collection_name="deck", record=test_deck1)
    db.save_record(collection_name="deck", record=test_deck2)
