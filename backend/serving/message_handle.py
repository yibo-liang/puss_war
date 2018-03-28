from serving.client_wsocket import ClientWSocketManager
from serving.PROTOCOL_CONSTS import *
import json


def make_message(type, msg):
    res = {
        "type": type,
        "content": msg
    }
    j = json.dumps(res)
    return j


def c_text(client_ws, data):
    print("Message from {} : {}".format(client_ws.address, data))


def check_auth(data):
    from authentication.authmanager import AuthManager
    cookie = data["cookie"]
    return AuthManager.is_user_authenticated(cookie)


def c_try_login(client_ws, data):
    from authentication.authmanager import AuthManager
    try:
        username = data["username"]
        password = data["password"]
    except:
        client_ws.send(make_message(S_LOGIN_FAIL, "请输入用户名和密码。"))
    cookie, msg = AuthManager.login((username, password))
    if cookie is not None:
        client_ws.cookie = cookie
        ClientWSocketManager.add_new_wsocket(cookie, client_ws)
    client_ws.send(msg)


def c_game(client_ws, data):
    client_ws.current_game.add_critic_message(client_ws.cookie, data)


def c_join_normal_queue(client_ws, data):
    if not check_auth(data):
        client_ws.send(make_message(S_LOGIN_FAIL, "非法操作，请重新登录。"))
    from game_matching.queue_manager import QueueManager

    # info = (cookie, deck_index, cat_index)
    QueueManager.join_queue((data["cookie"], data["deck_i"], data["cat_i"]))


def c_exit_normal_queue(client_ws, data):
    if not check_auth(data):
        client_ws.send(make_message(S_LOGIN_FAIL), "非法操作，请重新登录。")
        return
    from game_matching.queue_manager import QueueManager
    done = QueueManager.exit_queue(data["cookie"])
    if done:
        client_ws.send(make_message(S_EXIT_NORMAL_QUEUE_SUCCESS, {}))
    else:
        # ignore request, the player will be popped into game automatically
        pass


def disconnect(clienet_wss):
    from authentication.authmanager import AuthManager
    if clienet_wss.cookie is not None:
        AuthManager.logout_cookie(clienet_wss.cookie)
        ClientWSocketManager.remove_wsocket(clienet_wss.cookie)
