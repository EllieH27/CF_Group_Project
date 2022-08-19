import os
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
address = ("127.0.0.1",21)
handler = FTPHandler
auth = DummyAuthorizer()
handler.authorizer = auth
auth.add_user('testUser', 'Pa$$w0rd', '.', perm='elradfmwMT')
auth.add_anonymous(os.getcwd())
handler.banner = "Welcome to the server"
server = FTPServer(address,handler)
server.serve_forever()
auth.add_user()