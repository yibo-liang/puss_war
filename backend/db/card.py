from db._db_interface import *


class CardDBInterface:

    @staticmethod
    def get_card_by_id(id):
        try:
            db = NoSQLDatabase()
            db.init()
            u = db.find_one_by_key("_id", id, "card")
        except Exception as ex:
            print("ERROR")
            raise ex
        return u

    @staticmethod
    def update_deck(deck):
        pass

    @staticmethod
    def get_cards_by_deck(id):
        try:
            db = NoSQLDatabase()
            db.init()
            deck = db.find_one_by_key("_id", id, "deck")
            apostle_cards = deck["apostle_cards"]
            r1 = []
            for c in apostle_cards:
                card = db.find_one_by_key("_id", c["card_id"], "card")
                r1.append(card)

            cat_cards = deck["cat_cards"]
            r2 = []
            for c in cat_cards:
                card = db.find_one_by_key("_id", c["card_id"], "card")
                r2.append(card)
            print("r1",r1)
            print("r2",r2)
        except Exception as ex:
            print("ERROR")
            raise ex
        return {
            "apostle_cards": r1,
            "cat_cards": r2
        }


def dev_init():
    # Deck : id, title, cards(list of obj{card_id, info})

    print("Initialise card")
    db = NoSQLDatabase()
    db.init()
    # Card : id, title, description, thumbnail
    test_card1 = {
        "_id": 1,
        "type": "apostle",
        "title": "attack",
        "description": "Apostle Attack once",
        "visibility":"default",
        "thumbnail": ""
    }
    test_card2 = {
        "_id": 2,
        "type": "apostle",
        "title": "dodge",
        "description": "Avoid next attack within 2 rounds",
        "visibility": "default",
        "thumbnail": ""
    }
    test_card3 = {
        "_id": 10001,
        "type": "cat",
        "title": "attack",
        "description": "Cat Attack once",
        "visibility": "default",
        "thumbnail": ""
    }
    test_card4 = {
        "_id": 10002,
        "type": "cat",
        "title": "dodge",
        "description": "Avoid next attack within 2 rounds",
        "visibility": "default",
        "thumbnail": ""
    }
    db.save_record(collection_name="card", record=test_card1)
    db.save_record(collection_name="card", record=test_card2)
    db.save_record(collection_name="card", record=test_card3)
    db.save_record(collection_name="card", record=test_card4)
