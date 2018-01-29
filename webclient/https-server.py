import http.server, ssl

server_address = ('localhost', 4443)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket,
                               server_side=True,
                               certfile='server.pem',
                               keyfile="key.pem",
                               ssl_version=ssl.PROTOCOL_TLSv1)
print("Running")
httpd.serve_forever()