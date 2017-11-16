# typethief/server/eventqueue.py

import heapq
import threading


class Empty(Exception):
    pass


class EventQueue(object):
    """
    A thread-safe priority queue for events
    Not using python's queue.PriorityQueue since cannot peek timestamp of first
        element
    """
    def __init__(self):
        self._events = []
        self._mutex = threading.Lock()

    def empty(self):
        with self._mutex:
            return len(self._events) == 0

    def size(self):
        with self._mutex:
            return len(self._events)

    def put_event(self, timestamp, event):
        with self._mutex:
            heapq.heappush(self._events, (timestamp, event))

    def get_event(self):
        with self._mutex:
            if len(self._events) == 0:
                raise Empty
            else:
                timestamp, event = heapq.heappop(self._events)
                return event

    def peek_timestamp(self):
        with self._mutex:
            if len(self._events) == 0:
                raise Empty
            else:
                timestamp, event = self._events[0]
                return timestamp
