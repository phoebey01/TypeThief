# run_server.py

from typethief.server.views import app
from typethief.server.views import socketio


if __name__ == '__main__':
    socketio.run(app)
