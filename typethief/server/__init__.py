# typethief/server/__init__.py

from __future__ import print_function
import threading

from flask import copy_current_request_context
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
        self._rooms = {} # room_id: room
        super(_ServerNamespace, self).__init__(*args, **kwargs)


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
        self._rooms[new_room.id] = new_room

        @copy_current_request_context
        def handle_events(room):
            while room.id in self._rooms:
                for player_id, (event_type, event_body) in room.execute():
                    response = {'player_id': player_id}

                    if event_type == 'claim':
                        response['pos'] = event_body['pos']
                    elif event_type == 'play':
                        reponse = {}

                    emit(event_type, response, room=room.id, namespace=self.namespace)

        t = threading.Thread(target=handle_events, args=(new_room,))
        t.daemon = True
        t.start()

        response = {'player_id': new_player.id, 'room': new_room.encode()}
        join_room(new_room.id)
        join_room(new_player.id) # allow messaging to speific client
        emit('new_room_response', response)

    def on_input(self, message):
        # message = {'player_id':, 'room_id':, 'timestamp':, 'key':,}
        self._rooms[message['room_id']].add_event(
            message['player_id'],
            message['timestamp'],
            'input',
            {'key': message['key']},
        )

    def on_play(self, message):
        # message = {'player_id':, 'room_id':, 'timestamp':,}
        self._rooms[message['room_id']].add_event(
            message['player_id'],
            message['timestamp'],
            'play',
            {},
        )


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
        self._socketio.run(self._app)
        # self._server_socket_thread.start()
        # while True:
        #     # todo: process events
        #     pass
