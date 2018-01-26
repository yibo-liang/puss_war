class User:
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name
        self.current_game_id = None
        self.status = 0

        # user state
        # 0 default, doing nothing
        # 1 in queue
        # 2 game matched, waiting user to connect
        # 3 game matched, user connected
