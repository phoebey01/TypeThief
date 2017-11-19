# typethief/server/roomcontrol.py

import threading

from .eventqueue import Empty
from .eventqueue import EventQueue
from typethief.shared.room import Room


class RoomControlException(Exception):
    pass


class Playing(RoomControlException):
    pass


class Finished(RoomControlException):
    pass


class RoomControl(Room):
    """
    Rooms augmented with queues for each player
    """
    def __init__(self):
        self._player_queues = {}
        super().__init__()

    def _new_queue(self, player_id):
        if player_id not in self._player_queues:
            self._player_queues[player_id] = (EventQueue(), threading.Lock())

    def _delete_queue(self, player_id):
        if player_id in self._player_queues:
            del self._player_queues[player_id]

    def add_player(self, player):
        super().add_player(player)
        self._new_queue(player.id)

    def remove_player(self, player):
        self._delete_queue(player.id)
        super().remove_player(player.id)

    def add_event(self, player_id, timestamp, event_type, event_body):
        # will raise KeyError if queue doesnt exist
        q, lock = self._player_queues[player_id]
        with lock:
            q.put_event(timestamp, (event_type, event_body))

    def _handle_event(self, player_id, event):
        event_type, event_body = event

        if self._state == 'playing' and event_type == 'input':
            pos = self._text.claim_next(self._players[player_id], event_body['key'])
            if pos != None:
                return player_id, ('claim', {'pos': pos})
        elif self._state == 'waiting' and event_type == 'play':
            self.state = 'playing'
            return player_id, ('play', {})

        return None

    def execute(self):
        try:
            gvt = min([q.peek_timestamp() for q, lock in self._player_queues.values()])
        except Empty:
            return []

        executable_events = []
        for player_id, (q, lock) in self._player_queues.items():
            with lock:
                while not q.empty() and q.peek_timestamp() == gvt:
                    executable_events.append((player_id, q.get_event()))

        executed_events = []
        for player_id, e in executable_events:
            handled = self._handle_event(player_id, e)
            if handled:
                executed_events.append(handled)

        return executed_events
