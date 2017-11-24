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

    def _emit_error(message):
        emit('error', {'error': message})

    def on_connect(self):
        print('[Client connected]')

    def on_disconnect(self):
        # todo: add leaving
        print('[Client disconnected]')

    def _join_room(self, room=None):
        """
        This function must be called in a request context
        """
        if not room:
            room = RoomControl()
            self._rooms[room.id] = room
        new_player = Player(player_id=request.sid)
        room.add_player(new_player)
        join_room(room.id)
        join_room(new_player.id) # allow messaging specific client
        return room, new_player

    def on_new_room(self, message):
        # message = {}
        new_room, new_player = self._join_room()

        @copy_current_request_context
        def handle_events(room):
            while room.id in self._rooms:
                for player_id, (event_type, event_body) in room.execute():
                    response = {'player_id': player_id}

                    if event_type == 'claim':
                        response['pos'] = event_body['pos']
                    elif event_type == 'play':
                        response = {}

                    emit(event_type, response, room=room.id, namespace=self.namespace)

        t = threading.Thread(target=handle_events, args=(new_room,))
        t.daemon = True
        t.start()

        response = {'player_id': new_player.id, 'room': new_room.encode()}
        emit('new_room_response', response)

    def on_join_room(self, message):
        # message = {'room_id':,}
        room = self._rooms[message['room_id']]
        if room.state != 'waiting':
            self._emit_error('Room has closed')
            return

        room, new_player = self._join_room(room=room)
        sender_response = {'player_id': new_player.id, 'room': room.encode()}
        emit('join_room_response', sender_response)
        room_response = {'player_id': new_player.id}
        emit('new_player', room_response, room=room.id)


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

    def on_get_rooms(self, message):
        # message = {}
        open_rooms = [
            room_id
            for room_id in self._rooms
            if self._rooms[room_id].state == 'waiting'
        ]
        response = {'rooms': open_rooms}
        emit('get_rooms_response', response)


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

    def run(self):
        self._socketio.run(self._app, host='0.0.0.0', port=5000)
