# from game_handler.game_entity import GameEntity
# from game_handler.game_thread import GameThread

import game_handler.game_entity as ge
import game_handler.game_thread as gt
import game_handler.game_event_handler as eh


class OperatorModifier:
    def __init__(self, operator):
        self.operator = operator



class GameOperator:

    def __init__(self, game_thread):
        self.game_thread = game_thread
        self.game_entity = None
        self.event_handler = None
        # if game_entity is not None:
        #     self.game_entity = game_entity

    def init(self):
        self.game_entity = self.game_thread.game_entity
        self.event_handler = self.game_thread.event_handler

    def draw_from_deck(self, unit_type, player_i):
        cards = self.game_entity.get_player_unit_cards(player_i, unit_type)
        deck_cards = [card for card in cards if card["position"] == "deck"]
        if len(deck_cards) > 0:
            deck_cards = sorted(deck_cards, key=lambda c: c["drawing_i"])
            next = deck_cards[0]
            next["position"] = "hand"
            card_drawn = next
            return True, card_drawn
        else:
            return False

    def discard_from_hand(self, player_i, card_uuid):
        cards = self.game_entity.get_player_cards(player_i)
        t = [card for card in cards if card["uuid"] == card_uuid][0]
        if len(t) > 0:
            card = t[0]
            if card["position"] == "hand":
                card["position"] = "grave"
            else:
                return False
            return True
        else:
            return False

    # visual effect only
    def play_card_pre(self, player_i, card_uuid):
        cards = self.game_entity.get_player_cards(player_i)
        t = [card for card in cards if card["uuid"] == card_uuid][0]
        if len(t) == 1:
            card = t[0]
            # playing position is where card is being played by player and displayed to all
            card["position"] = "playing"
            card["visibility"] = "all"
            return True
        else:
            return False

    # play card ongoing, which will trigger play card event, and use the operator of the card
    def use_card_operator(self, player_i, card_handler):
        pass


    # visual effect only
    def play_card_post(self, player_i, card_uuid):
        cards = self.game_entity.get_player_cards(player_i)
        t = [card for card in cards if card["uuid"] == card_uuid][0]
        if len(t) == 1:
            card = t[0]
            if card["position"] == "playing":
                # playing position is where card is being played by player and displayed to all
                card["position"] = "grave"
                card["visibility"] = "all"
                return True
            else:
                return False
        else:
            return False
