import threading
import time
import queue
import game_core
import game_matching
from user import User
from game_core import *
from game_matching import *
import logging
from SimpleWebSocketServer import SimpleSSLWebSocketServer, WebSocket, SimpleWebSocketServer
import uuid
from helper import threadsafe


class connected_wsclient:
    def __init__(self, client_websocket_info=None, client_socket=None):
        # A connected client uses either websocket or normal socket
        self.id = str(uuid.uuid4())
        self.client_websocket = client_websocket_info["client"]
        self.server_websocket = client_websocket_info["server"]
        if self.server_websocket.connections is None:
            self.server_websocket.connections = {}

        self.server_websocket.on_receive[self.id] = None  #
        # normal socket, not implemented yet
        self.client_socket = client_socket  # TODO

    def send_to_client(self, msg):
        if connected_wsclient is not None:
            self.server_websocket.send_message(self.client_websocket, msg)
        else:
            raise Exception("Unimplemented Socket Handler")
            pass


#
# class game_server_thread(threading.Thread):
#     active_games = {}  # dictionary of game entity
#     wsserver = None
#
#     def init(self, wsserver, server_status):
#         game_server_thread.wsserver = wsserver
#         self.server_status = server_status
#
#     def run(self):
#         def new_client(wsclient, server):
#             connection = connected_wsclient(client_websocket_info={
#                 "server": server,
#                 "client": wsclient
#             })
#
#             thread = game_core.user_game_initialising_thread(connection, self.server_status)
#             thread.start()
#             # update server status, adding current thread to it
#             ss = self.server_status.get()
#             ss.connection_threads.append(thread)
#             self.server_status.put(ss)
#
#         @threadsafe
#         def on_message(client, server, message):
#             for game_id in game_server_thread.active_games:
#                 game = game_server_thread.active_games[game_id]
#
#
#         port = 8083
#         game_server_thread.wsserver = WebsocketServer(port, host='127.0.0.1', loglevel=logging.INFO)
#         game_server_thread.wsserver.set_fn_new_client(new_client)
#         game_server_thread.wsserver.set_fn_message_received(on_message)


class normal_user_thread(threading.Thread):
    def __init__(self, socket, server_status):
        threading.Thread.__init__(self)
        self.socket = socket
        self.server_status = server_status

    def run(self):
        print("Conected user")
        handle_normal_user_connection(self.socket)


def handle_normal_user_connection(socket):
    return 0


def listen_websocket(port):
    return 0


class session_websocket(WebSocket):
    def handleMessage(self):
        pass

    def handleConnected(self):
        self.sendMessage("Connected")
        print("connect")
        print(self.address)
        self.session_id = None
        self.cookie = None
        self.username = None

    def handleClose(self):
        pass


# for now we use only  ws, not wss
def user_session_wsserver(server_status):
    host = "localhost"
    port = 4334
    socket_class = session_websocket
    cert = "./webclient/server.pem"
    key = "./webclient/key.pem"
    server = SimpleSSLWebSocketServer(host, port, socket_class, cert, key)
    #server = SimpleWebSocketServer(host=host, port=port)
    print("wss ready to serve")
    server.serveforever()


# server for user connected, helps with user actions
# def user_general_wsserver(server_status):
#     # when user connect, this web socket server deals with login and user state
#     port = 8080
#     while (True):
#         socket = listen_websocket(port)
#
#         # start new thread with connected user
#         # new thread with handle_normal_user_connection(socket)
#         thread = normal_user_thread(socket, server_status)
#         thread.start()
#         # update server status
#         ss = server_status.get()
#         ss.connection_threads.append(thread);
#         server_status.put(ss)


#
# actual game server, deals with user game actions, and server update of the game
# update chat as well
def user_game_wsserver(server_status):
    # game thread creation, create
    pass


    #
    # def start_wsserver():
    #     port = 8083
    #     server = WebsocketServer(port, host='127.0.0.1', loglevel=logging.INFO)
    #     server.set_fn_new_client(new_client)
    #     ss = server_status.get()
    #     ss.game_wsserver = server
    #     server_status.put(ss)
    #     server.run_forever()
    #
    # threading.Thread(target=start_wsserver)
    #
    # port = 8081


def main():
    print("Initialising")

    # global sync waiting list
    sync_waiting_list = queue.Queue()
    waithing_list = []
    sync_waiting_list.put(waithing_list)

    # global game status
    sync_server_status = queue.Queue()
    server_status = {
        "game_wsserver": None,
        "login_wsserver": None,
        "active_users": [],
        "connection_threads": [],
        "game_matcher": None
    }
    sync_server_status.put(server_status)

    # start server thread
    # 1. server thread start websocket listening
    threading.Thread(target=user_session_wsserver(server_status)).start()
    # 2. start game match server thread
    matcher = Game_matcher()
    matcher.start()
    # 3. start user game server thread


    # print current running game

    return


main()
