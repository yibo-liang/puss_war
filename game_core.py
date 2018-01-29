import threading
import queue
from helper import threadsafe


# This thread is runing for each time a user is starting a game
class user_game_initialising_thread(threading.Thread):
    def __init__(self, connection, server_status):
        threading.Thread.__init__(self)
        # game socket , not for login or chat
        self.connection = connection
        self.server_status = server_status

    def run(self):
        print("Game thread for user")
        # get user by getting user cookie token from socket

        # get game by using game id this user is current at.

        # game get from server_status.active_game

        # add {userid, connection} to the game,

        # end


class Game_entity:
    lock = threading.Lock()
    current_game_count = 0
    total_game_count = 0
    active_games = {}

    def __del__(self):
        Game_entity.lock.acquire()
        Game_entity.current_game_count -= 1
        Game_entity.active_games.pop(self.id)
        Game_entity.lock.release()

    def __init__(self, users, server_status):

        def new_game(self):
            Game_entity.lock.acquire()
            Game_entity.total_game_count += 1
            Game_entity.current_game_count += 1

            self.game_id = Game_entity.total_game_count
            Game_entity.active_games[self.game_id] = self
            Game_entity.lock.release()

        # basic information
        self.users = users
        self.server_status = server_status
        new_game(self)
        self.msg_queue = queue.Queue()

        # card game information

        # game state:
        # 0 game waiting for users
        # 1 game running on first hand
        # 2 game running on second hand
        #
        self.game_state = 0

        # game round
        self.game_round = 1

        # game action queue, will be executed when player is at each state, of each round
        def new_round_actions_queues():
            return {
                "pre_drawing_actions": queue.Queue(),
                "post_drawing_actions": queue.Queue(),

                "pre_play_actions": queue.Queue(),
                "current_actions": queue.Queue(),
                "post_play_actions": queue.Queue(),

                "pre_discard_actions": queue.Queue(),
                "post_discard_actions": queue.Queue(),
            }

        self.queues = {
            1: new_round_actions_queues()
        }

        # action watcher queue, when before, during, or after each action is being executed
        # this list will be traversed and executed
        # can be used to handle passives
        self.action_watchers = None

        # current_hand, 0 or 1 in order
        self.current_hand = 0

        # game speed, the number of accumulation per second
        self.game_speed = 1

        # play order, should be random
        self.play_order = {
            0: "uid",
            1: "uid"
        }

        # player info
        self.players = {
            "uid": {

                "hand": "first/second",
                "cat": {
                    "cat_id": None,
                    "items": [],
                    "ability_id": 0,
                    "hp": 0,
                },
                "agent": {
                    "agent_id": None,
                    "items": [],
                    "hp": 0
                },
                # card information
                "deck": [],  # a list of cards
                "current_deck": [],  # list of current deck in this active game, not used for logic, only for display
                # current deck should be equal to draw_pile + grave_yard + consumed, a subset of deck
                "draw_pile": [],  # list of cards in draw pile
                "grave_yard": [],  # list of cards used and put into grave
                "consumed": [],  # list of cards removed from current game,
                "acting_point": 0.0,  # a float slowly accumulate, each card consumes specified points
                "threshold_acting_point": 0.0,  # the max acting_point to have, also the minimum to act

            }
        }

        # game history, can be used in the future for replay
        # TODO
        self.history = []

    def is_client_for_this_game(self, client_id):
        for uid in self.users:
            if self.users[uid] is not None and self.users[uid].wsclient_connection.id == client_id:
                return True
        return False

    def user_connect_game(self, user_id, wsclient_connection):
        self.users[user_id] = {
            "uid": user_id,
            "wsclient_connection": wsclient_connection
        }

    def check_user_connection(self):
        # check if user is connected, return boolean
        return False

    def toJSON(self, player):
        # return current game as a JSON string
        return ""
