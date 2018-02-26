from serving.client_wsocket import ClientWSocketManager


def c_text(client_ws, data):
    print("Message from {} : {}".format(client_ws.address, data))


def c_try_login(client_ws, data):
    from authentication.authmanager import AuthManager
    username = data["username"]
    password = data["password"]
    cookie, msg = AuthManager.login((username, password))
    if cookie is not None:
        client_ws.cookie = cookie
        ClientWSocketManager.add_new_wsocket(cookie, client_ws)
    client_ws.send(msg)


def c_game(client_ws, data):
    client_ws.current_game_msg_queue.put(data)


def disconnect(clienet_wss):
    from authentication.authmanager import AuthManager
    if clienet_wss.cookie is not None:
        AuthManager.logout_cookie(clienet_wss.cookie)
        ClientWSocketManager.remove_wsocket(clienet_wss.cookie)
