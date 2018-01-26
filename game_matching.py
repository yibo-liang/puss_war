import threading
import time

class game_matcher_thread(threading.Thread):
    def __init__(self, server_status, waiting_list):
        self.waiting_list = waiting_list
        self.server_status = server_status

    def run(self):
        print("game matcher starts working")

        while (True):

        # search through waiting list
        # find 2 players that matches, remove them from list
        # create game thread with game_id, use game_id as key in server status.active_games
        # send game_id to matched users
        # update waiting list
            time.sleep(0.01)
