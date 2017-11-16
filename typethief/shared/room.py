# typethief/shared/room.py

from collections import defaultdict

import pygame
from .clock import Clock
from .player import Player
from .text import Text


class Room(object):
    """
    Represents the state of a single game
    """
    _next_room = 0

    def __init__(self, encoded=None):
        if encoded:
            self.decode(encoded)
            return

        self._text = Text()
        self._players = defaultdict(lambda: None)
        self._room_id = Room._new_room_id()
        self._clock = Clock()

    def encode(self):
        encoded_players = {k: v.encode() for k, v in self._players.items()}
        return {
            'text': self._text.encode(),
            'players': encoded_players,
            'id': self._room_id,
            'time': self._clock.epoch,
        }

    def decode(self, encoded):
        self._text = Text(encoded=encoded['text'])
        self._players = defaultdict(
            lambda: None,
            {k: Player(encoded=v) for k, v in encoded['players'].items()},
        )
        self._room_id = encoded['id']
        self._clock = Clock(epoch=encoded['time'])

    @property
    def text(self):
        return self._text

    @property
    def id(self):
        return self._room_id

    @property
    def time(self):
        return self._clock.time

    @classmethod
    def _new_room_id(cls):
        room_id = 'room' + str(cls._next_room)
        cls._next_room += 1
        return room_id

    def get_player(self, player_id):
        return self._players[player_id]

    def add_player(self, player):
        self._players[player.id] = player

    def remove_player(self, player_id):
        del self._players[player_id]
