import threading
import time


class QueueManager:
    normal_queue = []  # a queue of active user cookie

    _lock = threading.Lock()

    @staticmethod
    def join_queue(cookie):
        QueueManager._lock.acquire()
        QueueManager.normal_queue.append(cookie)
        QueueManager._lock.release()

    @staticmethod
    def get_queue_size():
        return len(QueueManager.normal_queue)

    @staticmethod
    def remove_from_queue(cookie):
        QueueManager._lock.acquire()
        for i in range(len(QueueManager.normal_queue)):
            if QueueManager.normal_queue[i].id == cookie.id:
                QueueManager.normal_queue.pop(i)
                break
            i += 1
        QueueManager._lock.release()

    @staticmethod
    def match_players():

        def is_available(cookie):
            from authentication.authmanager import AuthManager
            from serving.communication import ClientWSocketManager
            return AuthManager.is_user_authenticated(cookie) \
                   and ClientWSocketManager.get(cookie) is not None

        QueueManager._lock.acquire()
        if QueueManager.get_queue_size() < 2:
            QueueManager._lock.release()
            return None
        # Dummy match maker, always find top 2 players
        cookie1 = QueueManager.normal_queue.pop(0)
        # double check if both users are online and authenticated user
        if not is_available(cookie1):
            QueueManager._lock.release()
            return None
        cookie2 = QueueManager.normal_queue.pop(0)
        # double check if both users are online and authenticated user
        if not is_available(cookie2):
            QueueManager.normal_queue.append(cookie1)
            QueueManager._lock.release()
            return None
        QueueManager._lock.release()
        return cookie1, cookie2

    @staticmethod
    def start_matching_service():

        def s():
            from game_matching.game_creator import MatchedGameManager
            while True:
                cookies = QueueManager.match_players()
                if cookies is None:
                    time.sleep(1)
                MatchedGameManager.add_matched_player(cookies)

        threading.Thread(target=s).start()
