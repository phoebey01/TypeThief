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


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class _ServerNamespace(Namespace):
    def __init__(self, *args, **kwargs):
        self._rooms = {} # room_id: room
        super(_ServerNamespace, self).__init__(*args, **kwargs)

    def _emit_error(message):
        emit('error', {'error': message})

    def on_connect(self):
        pass

    def on_disconnect(self):
        player_id = request.sid
        room = None
        for rm in self._rooms.values():
            if rm.get_player(player_id):
                room = rm
                break

        if room:
            room.remove_player(player_id)
            room_alert = {'player_id': player_id}
            if room.empty():
                del self._rooms[room.id]
            else:
                emit('player_quit', room_alert, room=room.id)

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

    def _add_event(self, room_id, *args):
        if room_id in self._rooms:
            self._rooms[room_id].add_event(*args)

    def _handle_events(self, room, emit_fun):
        while room.id in self._rooms:
            for player_id, (event_type, event_body) in room.execute():
                response = {'player_id': player_id}

                if event_type == 'claim':
                    response['pos'] = event_body['pos']
                elif event_type == 'play':
                    response = {}

                emit_fun(event_type, response, room.id)

    def on_new_room(self, message):
        # message = {}
        new_room, new_player = self._join_room()

        @copy_current_request_context
        def emit_with_context(event_type, response, room_id):
            emit(event_type, response, room=room_id, namespace=self.namespace)

        # improve performance 
        for i in xrange(3):
            t = threading.Thread(target=self._handle_events, args=(new_room, emit_with_context))
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
        self._add_event(
            message['room_id'],
            message['player_id'],
            message['timestamp'],
            'input',
            {'key': message['key']},
        )

    def on_play(self, message):
        # message = {'player_id':, 'room_id':, 'timestamp':,}
        self._add_event(
            message['room_id'],
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

    def on_null(self, message):
        self._add_event(
            message['room_id'],
            message['player_id'],
            message['timestamp'],
            'null',
            {},
        )

    def on_leave_room(self, message):
        room = self._rooms[message['room_id']]
        room.remove_player(message['player_id'])
        room_response = {'player_id': message['player_id']}
        emit('leave_room_response', room_response)
        
        if room.empty():
            del self._rooms[message['room_id']]
        else:
            emit('player_quit', room_response, room=room.id)


class Server(object):
    """
    Server represents the game server, and encapsulates everythong about it.
    This includes the flask app, socket app, views, and event handlers.
    """
    # todo: factor in address and port
    def __init__(self, config, host=None, port=None):
        self._app = Flask(__name__)
        self._app.config.from_object(config)
        self._host = config.SERVER_HOST if not host else host
        self._port = config.SERVER_PORT if not port else port

        self._socketio = SocketIO(self._app)
        self._socketio.on_namespace(_ServerNamespace('/play'))

    def run(self):
        self._socketio.run(self._app, host=self._host, port=self._port)
