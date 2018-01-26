import threading
import time
import queue
import game_core
import game_matching
from game_core import *
from game_matching import *

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


# server for user connected, helps with user actions
def web_server(server_status):
    # when user connect, this web socket server deals with login and user state
    port = 8080
    while (True):
        socket = listen_websocket(port)

        # start new thread with connected user
        # new thread with handle_normal_user_connection(socket)
        thread = normal_user_thread(socket, server_status)
        thread.start()
        # update server status
        ss = server_status.get()
        ss.connection_threads.append(thread);
        server_status.put(ss)


#
# actual game server, deals with user game actions, and server update of the game
# update chat as well
def user_game_server(server_status):

    # game thread creation, create
    def new_game_thread(socket, server_status):
        return 0

    port = 8081
    while (True):
        socket = listen_websocket(port)

        thread = new_game_thread(socket, server_status)
        thread.start()
        # update server status, adding current thread to it
        ss = server_status.get()
        ss.connection_threads.append(thread);
        server_status.put(ss)

def match_making_server(server_status,waiting_list):
    match_server_thread = game_matcher_thread(server_status, waiting_list)
    match_server_thread.run()

    return 0

def main():
    print("Initialising")

    # global sync waiting list
    sync_waiting_list = queue.Queue()
    waithing_list = []
    sync_waiting_list.put(waithing_list)

    # global game status
    sync_server_status = queue.Queue()
    server_status = {
        "active_users": [],
        "connection_threads": [],
        "active_games": {}
    }
    sync_server_status.put(server_status)

    # load users  //TODO database

    # start server thread
    # 1. server thread start websocket listening

    # 2. start game match server thread

    # 3. start user game server thread


    # print current running game

    return


main()
