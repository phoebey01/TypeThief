# typethief/server/__init__.py

import threading

from flask import Flask
from flask import request
from flask_socketio import emit
from flask_socketio import join_room
from flask_socketio import leave_room
from flask_socketio import Namespace
from flask_socketio import SocketIO
from .roomcontrol import RoomControl
from typethief.shared.player import Player


class _ServerNamespace(Namespace):
    def __init__(self, *args, **kwargs):
        self._rooms = {}
        super().__init__(*args, **kwargs)

    def on_connect(self):
        print('[Client connected]')

    def on_disconnect(self):
        # todo: add leaving
        print('[Client disconnected]')

    def on_new_room(self, message):
        # message = {}
        new_room = RoomControl()
        new_player = Player(player_id=request.sid)
        new_room.add_player(new_player)
        response = {'player_id': new_player.id, 'room': new_room.encode()}
        self._rooms[new_room.id] = new_room
        join_room(new_room.id)
        emit('new_room_response', response)


class Server(object):
    """
    Server represents the game server, and encapsulates everythong about it.
    This includes the flask app, socket app, views, and event handlers.
    """
    # todo: factor in address and port
    def __init__(self):
        self._app = Flask(__name__)
        self._socketio = SocketIO(self._app)
        self._socketio.on_namespace(_ServerNamespace('/play'))

        self._server_socket_thread = threading.Thread(
            target=self._socketio.run,
            args=(self._app,),
        )
        self._server_socket_thread.daemon = True

    def run(self):
        self._server_socket_thread.start()
        while True:
            # todo: process events
            pass
