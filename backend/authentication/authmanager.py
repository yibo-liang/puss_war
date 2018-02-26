import threading
import random
import time
from db._db_interface import NoSQLDatabase
from serving.PROTOCOL_CONSTS import *
from serving.communication import make_message as msg
from serving.MSG_CN import *
from db.user import UserDBInterface

import hashlib


def hash(text="default"):
    return hashlib.sha256(text.encode()).hexdigest()


class AuthManager:
    _lock_entity = threading.Lock()

    # authorised users
    _auth_users = {}

    @staticmethod
    def _lock():
        AuthManager._lock_entity.acquire()

    @staticmethod
    def _unlock():
        AuthManager._lock_entity.release()

    # Takes strings of username and password,
    # on success, return user session information, TODO persist session to db
    # on fail, return reason
    @staticmethod
    def login(auth_info):
        db = NoSQLDatabase()
        db.init()
        AuthManager._lock()
        username, password = auth_info

        u = UserDBInterface.get_user_by_username(username)
        m = msg(S_LOGIN_FAIL, UNKNOWN_ERROR_MSG)
        cookie = None
        if u is not None:
            passhash = hash(password)
            if passhash == u["password"]:
                t = time.time()
                cookie = hash("{}{}{}".format(t, username, random.random()))
                u["cookie"] = cookie
                # Remove credentials
                u.pop("password")
                u.pop("_id")

                result = u
                m = msg(S_LOGIN_SUCCESS, result)
                # Save cookie into dictionary for future query
                AuthManager._auth_users[cookie] = u, t
            else:
                m = msg(S_LOGIN_FAIL, UNAUTH_MSG)
        else:
            m = msg(S_LOGIN_FAIL, NON_EXIST_USER_MSG)
        # return the user
        AuthManager._unlock()
        return cookie, m

    @staticmethod
    def logout_cookie(cookie):

        AuthManager._lock()
        try:
            AuthManager._auth_users.pop(cookie)
        except:
            pass

        AuthManager._unlock()

    @staticmethod
    def get_user_by_cookie(cookie):
        u = AuthManager._auth_users[cookie]
        return u


    @staticmethod
    def is_user_authenticated(cookie):
        return AuthManager.get_user_by_cookie(cookie) is not None

    @staticmethod
    def auth_user_number():
        return len(AuthManager._auth_users.keys())
