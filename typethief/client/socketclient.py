# typethief/client/socketclient.py

import threading

from socketIO_client import SocketIO
from socketIO_client import BaseNamespace


class _TTNamespace(BaseNamespace):
    """
    """
    def on_connect(self):
        print('[Connected]')

    def on_reconnect(self):
        print('[Reconnected]')

    def on_disconnect(self):
        print('[Disconnected]')

    def on_new_room(self, data):
        print('new_room', data)


class SocketClient(object):
    """
    """
    def __init__(self, address, port, namespace='/play'):
        self._socketio = SocketIO(address, port)
        self._namespace = self._socketio.define(_TTNamespace, namespace)
        threading.Thread(target=self_socketio.wait, args=()).start()

    def new_room(self):
        self._namespace.emit('new_room', {})
