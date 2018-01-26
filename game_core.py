import threading

class user_game_thread(threading.Thread):
    def __init__(self, socket, server_status):
        threading.Thread.__init__(self)
        self.socket = socket
        self.server_status = server_status
        self.game_entity = None



    def run(self):
        print("Game thread for user")
        # get user by getting user cookie token from socket

        # get game using



class Game_entity:
    def __init__(self, users, server_status):
        self.users = users
        self.server_status = server_status

