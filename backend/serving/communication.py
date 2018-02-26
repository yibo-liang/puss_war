import json
import threading

from config import WEBSOCK_PORT
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from serving.PROTOCOL_CONSTS import *
from serving.message_handle import *


def make_message(type, msg):
    res = {
        "type": type,
        "content": msg
    }
    j = json.dumps(res)
    return j


import traceback, sys


def handle_message(client_wss, msg):
    msg = json.loads(msg)
    print("Handle messge : {}".format(msg))
    cases = {
        C_TEXT: c_text,
        C_TRY_LOGIN: c_try_login,
        C_GAME: c_game
    }
    case = msg["type"]
    print("Case = {}".format(case))
    if case is not None:
        try:
            cases[case](client_wss, msg)
        except Exception as ex:
            traceback.print_exc(file=sys.stdout)

    else:
        print("Client {} sent unknown message : {}".format(client_wss.address, msg))



class ClientWSocket(WebSocket):
    def __init__(self, server, sock, address):
        WebSocket.__init__(self, server, sock, address)
        self.cookie = None
        self.lock = threading.Lock()
        self.current_game_msg_queue = None

    def send(self, msg):
        s = json.dumps(msg)
        self.sendMessage(s)
        print("Sent {} to Client {}".format(s, self.address))

    def handleMessage(self):
        # lock for each message, so this ws is in fact sync
        self.lock.acquire()
        handle_message(self, self.data)
        self.lock.release()

    def handleConnected(self):
        self.lock.acquire()
        print("Client {} connected".format(self.address))
        try:
            # msg = build_message(msg="Connected")
            # self.sendMessage(msg)
            init_msg = make_message(S_INIT, [
                [S_TEXT, S_LOGIN_SUCCESS, S_LOGIN_FAIL],
                [C_TEXT, C_TRY_LOGIN]
            ])
            self.send(init_msg)

        except Exception:
            print(Exception)

        self.lock.release()

    def handleClose(self):
        if self.current_game_msg_queue is not None:
            self.current_game_msg_queue.put(make_message(C_IN_GAME_EXIT, {}))
        if self.cookie is not None:
            disconnect(self)


def session_wsserver():
    host = "localhost"
    port = WEBSOCK_PORT
    # cert = "./webclient/server.pem"
    # key = "./webclient/key.pem"
    # server = SimpleSSLWebSocketServer(host, port, socket_class, cert, key)
    server = SimpleWebSocketServer(host=host, port=port, websocketclass=ClientWSocket)
    print("WSServer ready to serve.")
    server.serveforever()


def start_wsserver():
    threading.Thread(target=session_wsserver).start()
