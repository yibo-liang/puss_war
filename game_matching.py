import threading
import time
import random
import queue


class Game_matcher(threading.Thread):
    lock = threading.Lock()
    waiting_list = []
    matched_players = queue.Queue()

    def add_to_waiting_list(self, user):
        Game_matcher.lock.acquire()
        # if already in waiting list, should be error, but ignore for now
        for u in Game_matcher.waiting_list:
            if u.uid == user.uid:
                Game_matcher.lock.release()
                return -1

        Game_matcher.waiting_list.append(user)
        Game_matcher.lock.release()

    def run(self):
        print("game matcher starts working")
        import game_core
        def naive_match():
            Game_matcher.lock.acquire()
            r = len(Game_matcher.waiting_list)
            if r < 2:
                return
            t1 = random.range(r)
            c1 = Game_matcher.waiting_list.pop(t1)
            t2 = random.random(len(r - 1))
            c2 = Game_matcher.waiting_list.pop(t2)
            Game_matcher.lock.release()
            # outside the lock, since queue is already sync by python
            Game_matcher.matched_players.put([c1, c2])

        while (True):
            naive_match()
            time.sleep(0.01)
