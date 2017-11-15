# typethief/shared/gamestate.py

from collections import defaultdict

import pygame
from player import Player
from text import Text


class GameState(object):
    """
    Represents the state of a single game
    """
    def __init__(self, encoded=None):
        if encoded:
            self.decode(encoded)
            return

        self._text = Text()
        self._players = defaultdict(lambda: None)
        self._time_diff = pygame.time.get_ticks()

    def encode(self):
        encoded_players = {k: v.encode() for k, v in self._players.items()}
        return {
            'text': self._text.encode(),
            'players': encoded_players,
            'time': pygame.time.get_ticks(),
        }

    def decode(self, encoded):
        self._text = Text(encoded=encoded['text'])
        self._players = defaultdict(
            lambda: None,
            {k: Player(encoded=v.decode()) for k, v in encoded['players'].items()},
        )
        self._time_diff = encoded['time'] - pygame.time.get_ticks()

    @property
    def time(self):
        return pygame.time.get_ticks() - self._time_diff

    @property
    def text(self):
        return self._text

    def get_player(self, player_id):
        return self._players[player_id]

    def add_player(self, player):
        self._players[player.id] = player

    def remove_player(self, player_id):
        del self._players[player_id]
