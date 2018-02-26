import threading
class ClientWSocketManager:
    active_wsockets = {}
    _lock = threading.Lock()

    @staticmethod
    def add_new_wsocket(cookie, sock):
        ClientWSocketManager._lock.acquire()
        ClientWSocketManager.active_wsockets[cookie] = sock
        ClientWSocketManager._lock.release()

    @staticmethod
    def remove_wsocket(cookie):
        ClientWSocketManager._lock.acquire()
        if cookie in ClientWSocketManager.active_wsockets:
            ClientWSocketManager.active_wsockets.pop(cookie)
        ClientWSocketManager._lock.release()

    @staticmethod
    def get(cookie):
        if cookie in ClientWSocketManager.active_wsockets:
            return ClientWSocketManager.active_wsockets[cookie]
        else:
            return None
