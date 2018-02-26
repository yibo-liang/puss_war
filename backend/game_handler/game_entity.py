# Entity Class for an active game

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
