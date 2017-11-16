# typethief/shared/player.py

from .text import Character


class Player(object):
    """
    Represents a typing player
    Each player has an id, claimed characters, and a score
    """
    _next_player = 0

    def __init__(self, encoded=None):
        """
        player_id [int]: player id
        encoded [dict]: encoded player; if provided, overrides other parameters
        """
        self._claimed = []
        self._score = 0

        if encoded:
            self.decode(encoded)
            return
        
        self._player_id = Player._new_player_id()

    def encode(self):
        encoded_claimed = [char.encode() for char in self._claimed]
        return {
            'player_id': self._player_id,
            'claimed': encoded_claimed,
        }

    def decode(self, encoded):
        self._player_id = encoded['player_id']
        self._claimed = []
        for e in encoded['claimed']:
            char = Character(encoded=e)
            self._claimed.append(char)
            self._score += char.val

    @property
    def score(self):
        return self._score

    @property
    def id(self):
        return self._player_id

    @classmethod
    def _new_player_id(cls):
        player_id = 'player' + str(cls._next_player)
        cls._next_player += 1
        return player_id

    def add_claimed(self, char):
        self._claimed.append(char)
        self._score += char.val