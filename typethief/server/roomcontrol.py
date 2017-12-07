# typethief/server/roomcontrol.py

import threading

from .eventqueue import Empty
from .eventqueue import EventQueue
from typethief.shared.room import Room


class RoomControl(Room):
    """
    Rooms augmented with queues for each player
    """
    def __init__(self):
        self._player_queues_lock = threading.Lock()
        self._player_queues = {}
        super(RoomControl, self).__init__()

    def _new_queue(self, player_id):
        with self._player_queues_lock:
            if player_id not in self._player_queues:
                self._player_queues[player_id] = EventQueue()

    def _delete_queue(self, player_id):
        with self._player_queues_lock:
            if player_id in self._player_queues:
                del self._player_queues[player_id]

    def add_player(self, player):
        super(RoomControl, self).add_player(player)
        self._new_queue(player.id)

    def remove_player(self, player_id):
        self._delete_queue(player_id)
        super(RoomControl, self).remove_player(player_id)

    def add_event(self, player_id, timestamp, event_type, event_body):
        with self._player_queues_lock:
            if player_id in self._player_queues: # must check since concurrent
                q = self._player_queues[player_id]
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
        gvt, qs = None, []
        try:
            with self._player_queues_lock:
                for player_id, q in self._player_queues.items():
                    if q.empty():
                        continue
                    timestamp = q.peek_timestamp()
                    if not gvt or timestamp < gvt:
                        gvt = timestamp
                        qs = [(player_id, q)]
                    elif timestamp == gvt:
                        qs.append((player_id, q))
                executable_events = [(pid, q.get_event()) for pid, q in qs]
        except KeyError as e:
            return []

        executed_events = []
        for player_id, e in executable_events:
            handled = self._handle_event(player_id, e)
            if handled:
                executed_events.append(handled)

        return executed_events
