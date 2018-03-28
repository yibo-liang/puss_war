import threading
import time


class QueueManager:
    normal_queue = []  # a queue of active user cookie

    _lock = threading.Lock()

    @staticmethod
    def join_queue(info):
        # info = (cookie, deck_index, cat_index)

        QueueManager._lock.acquire()
        QueueManager.normal_queue.append(info)
        QueueManager._lock.release()
        print("Join Queue with : {}".format(info))

    @staticmethod
    def exit_queue(cookie):
        print("Trying to Exit Queue")
        QueueManager._lock.acquire()
        found = False
        for i in range(len(QueueManager.normal_queue)):
            c, _, _ = QueueManager.normal_queue[i]
            if cookie == c:
                del QueueManager.normal_queue[i]
                found = True
                break

        QueueManager._lock.release()
        print("Queue Exit : {}".format(found))
        return found

    @staticmethod
    def get_queue_size():
        return len(QueueManager.normal_queue)

    @staticmethod
    def remove_from_queue(cookie):
        QueueManager._lock.acquire()
        for i in range(len(QueueManager.normal_queue)):
            info = QueueManager.normal_queue[i]
            _cookie, _, _ = info
            if _cookie == cookie:
                QueueManager.normal_queue.pop(i)
                break
            i += 1
        QueueManager._lock.release()

    @staticmethod
    def match_players():

        def is_available(cookie):
            print("Test is available {}"+cookie)
            from authentication.authmanager import AuthManager
            from serving.communication import ClientWSocketManager
            return AuthManager.is_user_authenticated(cookie) \
                   and ClientWSocketManager.get(cookie) is not None

        QueueManager._lock.acquire()
        if QueueManager.get_queue_size() < 2:
            QueueManager._lock.release()
            return None
        # Dummy match maker, always find top 2 players
        info1 = QueueManager.normal_queue.pop(0)
        _cookie1, _, _ = info1
        # double check if both users are online and authenticated user
        # print("cookie1={}",_cookie1)
        if not is_available(_cookie1):
            QueueManager._lock.release()
            return None
        info2 = QueueManager.normal_queue.pop(0)
        _cookie2, _, _ = info2

        # print("cookie2={}", _cookie2)
        # double check if both users are online and authenticated user
        if not is_available(_cookie2):
            QueueManager.normal_queue.append(_cookie2)
            QueueManager._lock.release()
            return None
        QueueManager._lock.release()
        return [info1, info2]

    @staticmethod
    def start_matching_service():
        print("Starting matching server...")

        def s():
            from game_matching.game_creator import MatchedGameManager
            while True:
                info = QueueManager.match_players()
                if info is None:
                    time.sleep(1)
                    continue
                MatchedGameManager.add_matched_player(info)
                print("Create new Match with {}".format(info))

        threading.Thread(target=s).start()
