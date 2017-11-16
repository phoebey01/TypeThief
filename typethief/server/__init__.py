# typethief/server/__init__.py

import threading

from flask import Flask
from flask_socketio import SocketIO
from .roomcontrol import RoomControl
from typethief.shared.player import Player


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

    def _make_views(self):
        @self._socketio.on('new_room')
        def handle_new_room(message):
            # message = {}
            new_room = RoomControl()
            new_player = Player()
            new_room.add_player(new_player)
            response = {'player_id': new_player.id, 'room': new_room.encode()}
            self._rooms[new_room.id] = new_room
            emit('new_room_response', response)

    def run(self):
        self._make_views()
        self._server_socket_thread.start()
        while True:
            # todo: process events
            pass
