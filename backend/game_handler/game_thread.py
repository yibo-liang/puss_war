import threading
import queue
from serving.communication import ClientWSocketManager
from serving.communication import make_message as msg
from authentication.authmanager import AuthManager
from serving.PROTOCOL_CONSTS import *

from game_handler.game_entity import GameEntity

from db.user import UserDBInterface
from abc import abstractmethod, ABCMeta, abstractproperty
from game_handler.exceptions import *


class PlaceHolder(object, metaclass=ABCMeta):

    @property
    @abstractmethod
    def game_thread(self):
        raise NotImplementedError("Player PlaceHolder : game_thread not implemented")

    @property
    @abstractmethod
    def type(self):
        raise NotImplementedError("Player PlaceHolder : type not implemented")

    @abstractmethod
    def play_term(self):
        raise NotImplementedError("Player PlaceHolder : play_term not implemented")


class HumanPlayer(PlaceHolder):

    def __init__(self, game_thread):
        self.game_thread = game_thread
        self.type = "Human"

    def play_term(self):
        pass


states = [
    "SYNC",
    "WAIT_DC",
    "",
    "WAIT_P2_RESPONSE"
]


# Game thread manages all process of an active game
# including communication with players, management of data flow,
class GameThread(threading.Thread):

    def __init__(self, cookies):

        self.initalisation = False
        self.player_cookies = cookies
        threading.Thread.__init__(self)
        self.msg_queues = {}
        self.client_socket = {}
        self.client_user_accounts = {}
        self.game_entity = None

    # Block and wait for client to reply a message with certain type
    # client identified by cookie
    # allow error is False by default, if client is disconnected while server is expecting, a error msg will be received
    def wait_client_message(self, cookie, msg_type, allow_error=False):
        while True:
            msg = self.msg_queues[cookie].get()
            if msg["type"] == msg_type:
                return msg
            else:
                if not allow_error:
                    return None

    def sync(self, data):
        for cookie in self.player_cookies:
            sock = self.client_socket[cookie]
            sock.send(msg(S_SYNC, data))
        for cookie in self.player_cookies:
            re = self.wait_client_message(cookie, C_SYNC_RE)
            if re is None:
                raise SynchronisationErrory("Synchroinsation faild for {}".format(cookie))

    def end(self):
        pass

    def run(self):

        # Init
        for cookie in self.player_cookies:
            self.msg_queues[cookie] = queue.Queue()
            sock = ClientWSocketManager.get(cookie)
            if sock is None:
                self.end()
                return

            # Fetch user id from auth manager, however fetch user information from db for the latest information
            user_id = AuthManager.get_user_by_cookie(cookie)["id"]
            self.client_user_accounts[cookie] = UserDBInterface.get_user_by_id(user_id)

            # give the message queue for player to wsocket of the client
            sock.current_game_msg_queue = self.msg_queues[cookie]
            self.client_socket[cookie] = sock

        self.sync({"sync_type": "game_start"})
        # If both replied, game starts from now,
        player_count = len(self.player_cookies)

        # Create Game entity to hold data of the game
        from random import randrange
        self.game_entity = GameEntity()
        ge = self.game_entity

        # Random select a starting player
        ge.current_player_i = randrange(0, player_count)

        # Load data from db for this game
        # User already loaded
