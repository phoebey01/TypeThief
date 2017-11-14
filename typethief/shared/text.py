# typethief/shared/text.py

class Character(object):
    """
    Represents a single character in a TypeThief text
    Each character has its position, char, and value
    """
    def __init__(self, position=None, char=None, value=None, encoded=None):
        """
        position [int]: index of character
        char [str]: single character
        value [int]: number of points character is worth
        encoded [dict]: encoded character; if provided, overrides other params
        """
        if encoded:
            self.decode(encoded)
            return
        self._position = position
        self._char = char
        self._value = value

    def encode(self):
        return {
            'position': self._position,
            'char': self._char,
            'value': self._value,
        }


    def decode(self, encoded):
        self._position = encoded['position']
        self._char = encoded['char']
        self._value = encoded['value']

    @property
    def pos(self):
        return self._position

    @property
    def c(self):
        return self._char

    @property
    def val(self):
        return self._value
