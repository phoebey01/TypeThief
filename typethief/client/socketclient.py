# typethief/client/socketclient.py

import threading

from socketIO_client import SocketIO
from socketIO_client import BaseNamespace


class _ClientNamespace(BaseNamespace):
    """
    Namespace that responds to messages from server
    Contains room because room needs to change based on serve rmessages
    """
    def __init__(self, *args, **kwargs):
        self._room = None # wait for server
        super().__init__(*args, **kwargs)

    @property
    def room(self):
        return self._room

    def on_connect(self):
        print('[Connected]')

    def on_reconnect(self):
        print('[Reconnected]')

    def on_disconnect(self):
        print('[Disconnected]')

    # todo: add responses


class SocketClient(object):
    """
    """
    def __init__(self, address, port, namespace='/play'):
        self._socketio = SocketIO(address, port)
        self._namespace = self._socketio.define(_ClientNamespace, namespace)

        self._receive_events_thread = threading.Thread(target=self._socketio.wait)
        self._receive_events_thread.daemon = True

    @property
    def room(self):
        return self._namespace.room

    def run(self):
        self._receive_events_thread.start()

    # todo: add sends
