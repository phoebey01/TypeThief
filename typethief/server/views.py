# typethief/server/views.py

import threading

from flask import Flask
from flask import jsonify
from flask import Response
from flask_socketio import SocketIO
from flask_socketio import emit


app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def api_root():
    return "index"


_next_room = 0
_next_mutex = threading.Lock()
@socketio.on('new_room', namespace='/play')
def on_newroom(data):
    global _next_room
    with _next_mutex:
        room = 'room' + str(_next_room)
        _next_room += 1
    emit('new_room', {'room_id': room})


# todo:
#   - create newplayer id
#   - add newplayer to game state
#   - send game state to new player
@socketio.on('join', namespace='/play')
def on_join(data):
    if 'room_id' not in data:
        emit('error', {'error': 'room_id not found'})
    else:
        room = data['room_id']
        join_room(room)
        emit('player_joined', {'player_id': 0}, room=room)


# todo:
#   - remove player from game state
@socketio.on('leave', namespace='/play')
def on_leave(data):
    if 'player_id' not in data:
        emit('error', {'error': 'player_id not found'})
    elif 'room_id' not in data:
        emit('error', {'error': 'room_id not found'})
    else:
        player, room = data['player_id'], data['room_id']
        leave_room(room)
        emit('player_left', {'player_id': player}, room=room)
