import hashlib
import threading
from pymongo import MongoClient


class nosql_db():
    def __init__(self, db_name):
        self.HOST = "localhost"
        self.PORT = 27017

        self.DB_NAME = db_name

        self.client = None
        self.db = None
        self.collection = None

    def init(self, collection):
        self.client = MongoClient(self.HOST, self.PORT)
        self.db = self.client[self.DB_NAME]
        self.collection = self.db[collection]

    def save_record(self, record):
        # print(record)
        self.collection.insert_one(record)
        return True

    def for_each_record(self, func):
        i = 0
        for document in self.collection.find():
            func(document)
            i += 1
            print("Doc i = %d" % i)


class User:
    def __init__(self):
        self.uid = 0
        self.username = ""
        self.password = ""  # hashlib.sha256("")
        self.cookie = ""

        self.name = ""
        self.current_game_id = None
        self.status = 0

        # user state
        # 0 default, doing nothing
        # 1 in queue
        # 2 game matched, waiting user to connect
        # 3 game matched, user connected


class UserManager:
    lock = threading.Lock()
    active_users = {}
    db = nosql_db("puss_war")

    dummy_count = 0

    def __init__(self):
        UserManager.db.init("users")

    def get_user_by_id(self, id):
        pass

    def get_user_by_cookie(self, id):
        pass

    def login_user(self, username, password):
        UserManager.lock.acquire()
        # auth user,
        u = User()
        u.username = username
        u.uid = UserManager.dummy_count
        u.cookie = hashlib.sha256(str(u.uid)).hexdigest()
        UserManager.dummy_count += 1

        # put user into active users
        UserManager.active_users[u.cookie]
        # return the user
        UserManager.lock.release()
        return u

    def logout_user(self, id=None, username=None, cookie=None):
        if id is not None:
            for cookie in UserManager.active_users:
                tmp = UserManager.active_users[cookie]
                if tmp.id == id:
                    UserManager.active_users.pop(tmp)
            return
        if username is not None:
            for cookie in UserManager.active_users:
                tmp = UserManager.active_users[cookie]
                if tmp.username == username:
                    UserManager.active_users.pop(tmp)
            return
        if cookie is not None:
            for tcookie in UserManager.active_users:
                if tcookie == cookie:
                    UserManager.active_users.pop(UserManager.active_users[cookie])
            return
