# Entity Class for an active game
import copy
import threading

G_INIT = 0
P_START = 10  # Player starts
P_DRAW = 20
P_PLAY = 30
P_DISCARD = 40
P_END = 50


class GameEntity:
    count = 0
    _lock = threading.Lock()

    def __init__(self):
        GameEntity._lock.acquire()
        self.id = GameEntity.count
        GameEntity.count += 1
        GameEntity._lock.release()

        self.current_player_i = 0
        self.state = G_INIT

        self.players = []
        # plyaer = { card player | npc player}
        # card player = {energy, [units]}
        # unit = {basic info, health, buff list, cards}
        # card = { card info, position, visibility, uuid}
        #   position = one of [deck, hand, grave, preparation, consumed]
        #   visibility = default (only me) | enemy only | all | none
        #   uuid : re-generated whenever a card is given to a player

    def get_player_cards(self, player_i):
        player = self.players[player_i]
        res = []
        for unit in player["units"]:
            res += unit["cards"]
        return res

    def get_player_unit_cards(self, player_i, unit_type):
        player = self.players[player_i]
        res = []
        for unit in player["units"]:
            if unit["type"] == unit_type:
                res += unit["cards"]
                break
        return res

    def entity_for_player(self, index):
        data = copy.deepcopy(self.__dict__)

        def filter_cards_by_visibility(cards, is_self):
            res = []
            for card in cards:
                v = card["visibility"]
                card.pop("_id")
                card.pop("drawing_i")
                if is_self:  # if is filtering player self's cards
                    if v == "enemy_only" or v == "none":  # if card is for enemy or none to know, hide all info
                        res.append({
                            "position": card["position"],
                            "uuid": card["uuid"],
                            "type": card["type"]
                        })
                    else:
                        res.append(card)
                else:  # if is filtering other players' cards
                    if v == "enemy_only" or v == "all":
                        res.append(card)
                    else:
                        res.append({
                            "position": card["position"],
                            "uuid": card["uuid"],
                            "type": card["type"]
                        })
            return res

        players = []
        all_cards = []

        player_i = 0
        # for each player
        for player in data["players"]:
            player["i"] = player_i
            unit_i = 0
            # for each unit that player controls
            for unit in player["units"]:
                unit["i"] = unit_i
                unit["cards"] = filter_cards_by_visibility(unit["cards"], player_i == index)

                # put all cards into one single list, because flattened data is better for frontend
                for card in unit["cards"]:
                    card["unit_i"] = unit_i
                    card["player_i"] = player_i
                    card["self"] = player_i == index
                    card["unit_type"] = unit["type"]
                    all_cards.append(card)
                unit.pop("cards")
                unit.pop("_id")
                # if not self
                if not player_i == index:
                    # When send to player i, he has all information of himself, but minimal info of enemy
                    if unit["type"] == "cat":
                        unit.pop("ability_id")
                unit_i += 1
            player["self"] = player_i == index
            players.append(player)
            player_i += 1
        data["players"] = players
        data["all_cards"] = all_cards
        return data

    # return winner i if game end, otherwise None
    def is_game_end(self):
        # for each player
        i = 0
        for player in self.players:
            all_dead = True
            for unit in player["units"]:
                if unit["health"] > 0:
                    all_dead = False
                    break
            if all_dead:
                return i
            i += 1
        return None

    def get_natural_drawing_count(self, player_i, unit_type):
        i = player_i
        player = self.players[i]
        unit = [unit for unit in player["units"] if unit["type"] == unit_type][0]
        count = unit["drawing_number"]
        return count

    def get_hand_card_nmumber(self, player_i, unit_type):
        player = self.players[player_i]
        unit = [unit for unit in player["units"] if unit["type"] == unit_type][0]
        return len(unit["cards"])

    def get_hand_card_capacity(self, player_i, unit_type):
        player = self.players[player_i]
        unit = [unit for unit in player["units"] if unit["type"] == unit_type][0]
        return len(unit["cards"])

    # def do_settlement(self, settlement):
    #
    #     # this function consists a set of sub function, each handles a settlement type
    #     # settlement handler changes game entity data, and returns front end update information
    #
    #     def draw_card(settlement):
    #         player_i = settlement["PLAYER_I"]
    #         player = self.players[player_i]
    #         unit = [u for u in player["units"] if u["type"] == settlement["UNIT_TYPE"]][0]
    #         deck_cards = [card for card in unit["cards"] if card["position"] == "deck"]
    #         deck_cards = sorted(deck_cards, key=lambda c: c["drawing_i"])
    #         next = deck_cards[0]
    #         next["position"] = "hand"
    #         return {
    #             "SETTLEMENT_RESULT": "UPDATE_CARD",
    #             "CARD_UUID": next["uuid"],
    #             "UPDATE": {
    #                 "position": "hand"
    #             }
    #         }
    #
    #     settlements = {
    #         "DRAW_CARD": draw_card,
    #         "PLAYER_ACTION": None
    #
    #     }
    #     key = settlement["SETTLEMENT"]
    #     return settlements[key](settlement)
