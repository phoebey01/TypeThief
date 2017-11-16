# typethief/client/socketclient.py

import threading

from socketIO_client import SocketIO
from socketIO_client import BaseNamespace
from typethief.shared.room import Room


class _ClientNamespace(BaseNamespace):
    """
    Namespace that responds to messages from server
    Contains room because room needs to change based on server messages
    """
    def __init__(self, *args, **kwargs):
        self._player_id = None
        self._room = None
        super().__init__(*args, **kwargs)

    @property
    def id(self):
        return self._player_id

    @property
    def room(self):
        return self._room

    def on_connect(self):
        print('[Connected]')

    def on_reconnect(self):
        print('[Reconnected]')

    def on_disconnect(self):
        print('[Disconnected]')

    def on_new_room_response(self, response):
        self._player_id = response['player_id']
        self._room = Room(encoded=response['room'])


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

    def run(self):
        self._receive_events_thread.start()

    def _send_new_room(self):
        self._namespace.emit('new_room', {})
