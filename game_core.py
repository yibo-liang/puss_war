import threading


class user_game_thread(threading.Thread):
    def __init__(self, socket, server_status):
        threading.Thread.__init__(self)
        # game socket , not for login or chat
        self.socket = socket
        self.server_status = server_status

    def run(self):
        print("Game thread for user")
        # get user by getting user cookie token from socket

        # get game by using game id this user is current at.

        # game get from server_status.active_game

        # add {userid, socket} to the game,

        # end


class Game_entity:
    def __init__(self, server_status):
        # basic information
        self.users = {}
        self.server_status = server_status
        self.game_id = None

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
                "pre_drawing_actions": None,
                "post_drawing_actions": None,

                "pre_play_actions": None,
                "current_actions": None,
                "post_play_actions": None,

                "pre_discard_actions": None,
                "post_discard_actions": None,
            }

        self.queues = {
            0: new_round_actions_queues()
        }

        # action watcher queue, when before, during, or after each action is being executed
        # this list will be traversed and executed
        # can be used to handle passives
        self.action_watchers = None

        # current_hand
        self.current_hand = "uid"

        # game speed, the number of accumulation per second
        self.game_speed = 1

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

    def user_connect_game(self, user_id, socket):
        self.users[user_id] = {
            "uid": user_id,
            "game_socket": socket
        }

    def check_user_connection(self):
        # check if user is connected, return boolean
        return False

    def toJSON(self, player):
        # return current game as a JSON string
        return ""
