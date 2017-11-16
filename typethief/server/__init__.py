# typethief/server/__init__.py

import threading

from flask import Flask
from flask_socketio import SocketIO


class Server(object):
    """
    Server represents the game server, and encapsulates everythong about it.
    This includes the flask app, socket app, views, and event handlers.
    """
    # todo: factor in address and port
    def __init__(self):
        self._app = Flask(__name__)
        self._socketio = SocketIO(self._app)
        self._rooms = {}

        self._server_socket_thread = threading.Thread(
            target=self._socketio.run,
            args=(self._app,),
        )
        self._server_socket_thread.daemon = True

    def run(self):
        # todo: create routes
        self._server_socket_thread.start()
        while True:
            # todo: process events
            pass
