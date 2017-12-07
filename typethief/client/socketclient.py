# typethief/client/socketclient.py

from __future__ import print_function

import threading

from socketIO_client import SocketIO
from socketIO_client import BaseNamespace
from typethief.shared.player import Player
from typethief.shared.room import Room


class _ClientNamespace(BaseNamespace):
    """
    Namespace that responds to messages from server
    Contains room because room needs to change based on server messages
    """
    def __init__(self, *args, **kwargs):
        super(_ClientNamespace, self).__init__(*args, **kwargs)

        self._player_id = None
        self._room = None
        self._open_rooms = [] # not considered intrinsic state  

    @property
    def id(self):
        return self._player_id

    @property
    def room(self):
        return self._room

    def get_open_rooms(self):
        return self._open_rooms[:]

    def on_connect(self):
        print('[Connected]')

    def on_reconnect(self):
        print('[Reconnected]')

    def on_disconnect(self):
        print('[Disconnected]')

    def on_new_room_response(self, response):
        # response: {'player_id':, 'room':,}
        self._player_id = response['player_id']
        self._room = Room(encoded=response['room'])

    def on_join_room_response(self, response):
        # response: {'player_id':, 'room':,}
        self._player_id = response['player_id']
        self._room = Room(encoded=response['room'])

        self._quit = False

    def on_claim(self, response):
        # response: {'player_id':, pos':,}
        player_id, pos = response['player_id'], response['pos']
        if pos == self._room.text.next_pos:
            self._room.text.claim_next(self._room.get_player(player_id))

    def on_play(self, response):
        # response: {}
        self._room.state = 'playing'

    def on_get_rooms_response(self, response):
        self._open_rooms = response['rooms']

    def on_new_player(self, response):
        # response: {'player_id':,}
        player_id = response['player_id']
        if not self._room.get_player(player_id):
            new_player = Player(player_id=player_id)
            self._room.add_player(new_player)

    def on_player_quit(self, response):
        # response: {'player_id':}
        player_id = response['player_id']
        if self._room:
            if self._room.get_player(player_id):
                self._room.remove_player(player_id)

    def on_leave_room_response(self, response):
        # remove room and player_id when quiting
        if response['player_id'] == self._player_id:
            self._room = None
            self._player_id = None


class SocketClient(object):
    """
    """
    def __init__(self, address, port, namespace='/play'):
        self._socketio = SocketIO(address, port)
        self._namespace = self._socketio.define(_ClientNamespace, namespace)

        self._receive_events_thread = threading.Thread(target=self._socketio.wait)
        self._receive_events_thread.daemon = True

    @property
    def player_id(self):
        return self._namespace.id

    @property
    def room(self):
        return self._namespace.room

    def _get_open_rooms(self):
        return self._namespace.get_open_rooms()

    def _message_prototype(self):
        return {
            'player_id': self._namespace.id,
            'room_id': self._namespace.room.id,
            'timestamp': self._namespace.room.time,
        }

    def _send_new_room(self):
        self._namespace.emit('new_room', {})

    def _send_join_room(self, room_id):
        message = {'room_id': room_id}
        self._namespace.emit('join_room', message)

    def _send_input(self, key):
        if not self.room:
            return
        message = self._message_prototype()
        message['key'] = key
        self._namespace.emit('input', message)

    def _send_play(self):
        if self.room.state == 'waiting':
            message = self._message_prototype()
            self._namespace.emit('play', message)

    def _send_get_rooms(self):
        self._namespace.emit('get_rooms', {})

    def _send_null(self):
        message = self._message_prototype()
        self._namespace.emit('null', message)

    def _send_leave_room(self):
        message = self._message_prototype()
        self._namespace.emit('leave_room', message)

    def run(self):
        self._receive_events_thread.start()
