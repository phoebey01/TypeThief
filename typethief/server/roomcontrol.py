# typethief/server/roomcontrol.py

import threading

from .eventqueue import EventQueue
from typethief.shared.room import Room


class RoomControl(Room):
    """
    Rooms augmented with queues for each player
    """
    def __init__(self):
        self._player_queues = {}
        super().__init__()

    def new_queue(self, player_id):
        if player_id not in self._player_queues:
            self._player_queues[player_id] = (EventQueue(), threading.Lock())

    def delete_queue(self, player_id):
        if player_id in self._player_queues:
            del self._player_queues[player_id]

    def add_event(self, player_id, timestamp, event_type, event_body):
        # will raise KeyError if queue doesnt exist
        q, lock = self._player_queues[player_id]
        with lock:
            q.put_event(timestamp, (event_type, event_body))

    # todo: handle event
    def _handle_event(self, player_id, event):
        event_type, event_body = event

    # todo: handle dead queue case
    def execute(self):
        gvt = min([q.peek_timestamp() for q in self._player_queues.values()])
        executable_events = []
        for player_id, (q, lock) in self._player_queues.items():
            with lock:
                while not q.empty() or q.peek_timestamp() == gvt:
                    executable_events.append((player_id, q.get_event()))
        for player_id, e in executable_events:
            self._handle_event(player_id, e)
        return executable_events
