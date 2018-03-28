import threading
import queue
from serving.communication import ClientWSocketManager
from serving.communication import make_message as msg
from authentication.authmanager import AuthManager
from serving.PROTOCOL_CONSTS import *

from game_handler.game_entity import GameEntity

from db import *

from abc import abstractmethod, ABCMeta, abstractproperty
from game_handler.exceptions import *

# helper function
from uuid import uuid4
import random
from queue import PriorityQueue


def _init_card(card):
    card["position"] = "deck"
    card["uuid"] = str(uuid4())
    return card


# Game thread manages all process of an active game
# including communication with players, management of data flow,
class GameThread(threading.Thread):

    def __init__(self, info):
        from game_handler.game_event_handler import GameEventsHandler
        from game_handler.game_operator import GameOperator
        from game_handler.game_settlement_handler import SettlementHandler
        self.initalisation = False
        self.player_cookies = [cookie for cookie, _, _ in info]
        # set up the map of information
        self.player_info = {}
        i = 0
        for cookie in self.player_cookies:
            self.player_info[cookie] = info[i]
            i += 1
        # -----------------------------
        threading.Thread.__init__(self)
        self.critic_msg_queues = {}
        self.casual_msg_queues = {}
        self.client_socket = {}
        self.client_user_accounts = {}
        self.game_entity = GameEntity()
        self.event_handler = GameEventsHandler(game_thread=self)
        self.game_operator = GameOperator(game_thread=self)
        self.settlement_handler = SettlementHandler(game_thread=self)

        self.event_handler.init()
        self.game_operator.init()
        self.settlement_handler.init()

        # game runtime
        self.state = "INIT"

    def add_critic_message(self, cookie, msg):
        self.critic_msg_queues[cookie].put(msg)

    def add_casual_message(self, cookie, msg):
        self.casual_msg_queues[cookie].put(msg)

    # Block and wait for client to reply a message with certain type
    # client identified by cookie
    # allow error is False by default, if client is disconnected while server is expecting, a error msg will be received
    def wait_client_message(self, cookie, msg_type, allow_error=False):
        while True:
            msg = self.critic_msg_queues[cookie].get()
            content = msg["content"]
            type = content["type"]
            if type == msg_type:
                return msg
            else:
                if not allow_error:
                    return None

    def broadcast(self, type, data):
        i = 0
        print("Braodcast:", data)
        for cookie in self.client_user_accounts:
            m = msg(S_G_SYNC, {"sync_type": type, "data": data})
            sock = self.client_socket[cookie]
            sock.send(m)
            i += 1

    def sync(self, type):

        ms = {}
        if type == "GAME_FULLDATA":
            i = 0
            for cookie in self.client_user_accounts:
                data = self.game_entity.entity_for_player(i)
                m = msg(S_G_SYNC, {"sync_type": "GAME_FULLDATA", "data": data})
                ms[cookie] = m
                i += 1
        elif type == "GAME_START":
            m = msg(S_G_SYNC, {"sync_type": "GAME_START"})
            for cookie in self.client_user_accounts:
                ms[cookie] = m

        i = 0
        for cookie in self.client_user_accounts:
            sock = self.client_socket[cookie]
            sock.send(ms[cookie])

        # No response for sync required
        # for cookie in self.client_user_accounts:
        #     re = self.wait_client_message(cookie, C_G_SYNC)
        #     if re is None:
        #         raise SynchronisationErrory("Synchroinsation faild for {}".format(cookie))

    def create_init_game_entity(self):

        # plyaer = { card player | npc player}
        # card player = {energy, [units]}
        # unit = {basic info, health, buff list, cards}
        # card = { card info, position, visibility, uuid}
        #   position = one of [deck, hand, grave, preparation, consumed]
        #   visibility = default (only me) | enemy only | all | none
        #   uuid : re-generated whenever a card is given to a player
        def prepare_cards(cards):
            random.shuffle(cards)
            res = []
            i = 0

            for card in cards:
                card["drawing_i"] = i
                res.append(card)
                i += 1
            return res

        # If both replied, game starts from now,
        player_count = len(self.player_cookies)

        # Create Game entity to hold data of the game
        from random import randrange
        ge = self.game_entity

        # Random select a starting player
        ge.current_player_i = randrange(0, player_count)

        # Load data from db for this game
        # User already loaded
        i = 0
        for cookie in self.client_user_accounts:
            u = self.client_user_accounts[cookie]
            _, deck_i, cat_i = self.player_info[cookie]

            cards = CardDBInterface.get_cards_by_deck(u["decks"][deck_i])
            # apostle
            print("apostle_cards", cards["apostle_cards"])
            apostle_cards = [_init_card(c) for c in cards["apostle_cards"]]
            # shuffle cards and assign card drawing order
            apostle_cards = prepare_cards(apostle_cards)

            _apostle = ApostleDBInterface.get_apostle_by_id(u["apostle_id"])
            _apostle["type"] = "apostle"
            _apostle["health"] = 50
            _apostle["max_health"] = 50
            _apostle["buffs"] = []
            _apostle["cards"] = apostle_cards
            _apostle["drawing_number"] = 2
            _apostle["hand_capacity"] = 4

            # cat
            cat_cards = [_init_card(c) for c in cards["cat_cards"]]
            cat_cards = prepare_cards(cat_cards)
            print("cat_cards", cards["cat_cards"])
            cat = CatDBInterface.get_cat_by_id(u["cats"][cat_i]["cat_id"])
            cat["type"] = "cat"
            cat["level"] = u["cats"][cat_i]["level"]
            cat["buffs"] = []
            cat["max_health"] = cat["health"]
            cat["cards"] = cat_cards
            cat["drawing_number"] = 2
            cat["hand_capacity"] = 4
            # overall
            player = {
                "type": "CARD",
                "i": i,
                "units": [cat, _apostle],
                "energy": 1,
            }
            i += 1
            ge.players.append(player)
        return ge

    def end(self):
        pass

    def new_settlement(self, settlement, priority):
        self.settlement_handler.new_settlement(settlement, priority)

    def do_settlement(self, settlement):
        return self.settlement_handler.do_settlement(settlement)
        # return self.game_entity.do_settlement(settlement)

    def do_next_state(self):
        state_transition = {
            "INIT": "START",
            "START": "DRAWING",
            "DRAWING": "PLAYING",
            "PLAYING": "DISCARDING",
            "DISCARDING": "END",
            "END": "SWITCH_PLAYER",
            "SWITCH_PLAYER": "START"
        }
        self.state = state_transition[self.state]

        def start():
            # TODO
            pass

        def drawing():
            count = self.game_entity.get_natural_drawing_count(self.game_entity.current_player_i, "cat")
            for i in range(count):
                self.new_settlement({
                    "SETTLEMENT": "DRAW_CARD",
                    "UNIT_TYPE": "cat",
                    "PLAYER_I": self.game_entity.current_player_i
                }, 100)

        def playing():
            # inform player to play,
            # wait for action
            cookie = self.player_cookies[self.game_entity.current_player_i]
            msg = self.wait_client_message(cookie, C_GAME_ACTION, False)
            content = msg["content"]
            allowed_actions = ["PLAY_CARD", "USE_ABILITY", "END_TERM", "SURRENDER"]
            if content["ACTION_TYPE"] in allowed_actions:
                self.new_settlement({
                    "SETTLEMENT": "PLAYER_ACTION",
                    "CONTENT": content
                }, 100)

        def discarding():
            # ask player to discard cards
            i = self.game_entity.current_player_i
            capacity = self.game_entity.get_natural_drawing_count(i, "apostle")
            hand_number = self.game_entity.get_hand_card_nmumber(i, "apostle")
            if hand_number > capacity:
                discard_count = hand_number - capacity
                self.new_settlement({
                    "SETTLEMENT": "DISCARD",
                    "PLAYER_I": i,
                    "NUMBER": discard_count,
                    "UNIT": "apostle"
                }, 100)
            capacity = self.game_entity.get_natural_drawing_count(i, "cat")
            hand_number = self.game_entity.get_hand_card_nmumber(i, "cat")
            if hand_number > capacity:
                discard_count = hand_number - capacity
                self.new_settlement({
                    "SETTLEMENT": "DISCARD",
                    "PLAYER_I": i,
                    "NUMBER": discard_count,
                    "UNIT": "cat"
                }, 100)

        def switch_player():
            i = self.game_entity.current_player_i
            i = 1 if i == 0 else 0
            self.new_settlement({
                "SETTLEMENT": "SWITCH_PLAYER",
                "NEXT": i
            }, 100)

        state_jobs = {
            "INIT": [],
            "START": [],
            "DRAWING": [drawing],
            "PLAYING": [playing],
            "DISCARDING": [discarding],
            "END": [],
            "SWITCH_PLAYER": [switch_player]
        }
        for job in state_jobs[self.state]:
            job()

    def run(self):
        print("**************  Game thread Starting... **************")
        # Init
        for cookie in self.player_cookies:
            self.critic_msg_queues[cookie] = queue.Queue()
            sock = ClientWSocketManager.get(cookie)
            if sock is None:
                self.end()
                return

            # Fetch user id from auth manager, however fetch user information from db for the latest information
            u, t = AuthManager.get_user_by_cookie(cookie)
            user_id = u["_id"]
            self.client_user_accounts[cookie] = UserDBInterface.get_user_by_id(user_id)

            # give the message queue for player to wsocket of the client
            sock.current_game = self
            self.client_socket[cookie] = sock

        self.sync("GAME_START")
        self.game_entity = self.create_init_game_entity()
        self.sync("GAME_FULLDATA")

        # while game not end
        #   if settlement queue not empty
        #   do settlement
        #   else
        #   enter next state
        #   sync
        #   check if game ends
        while not self.game_entity.is_game_end():

            settlement_result = self.settlement_handler.do_next_settlement()
            if settlement_result is not None:
                self.broadcast("SETTLEMENT", settlement_result)
            else:
                self.do_next_state()

            if self.state == "END":
                break

            # dummy
