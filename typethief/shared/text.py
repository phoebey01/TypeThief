# typethief/shared/text.py

import random
import re
import requests

from bs4 import BeautifulSoup


_TYPERACER_TEXTS_URL = 'http://www.typeracerdata.com/texts?texts=full&sort=relative_average'


def get_random_text():
    r = requests.get(_TYPERACER_TEXTS_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.select('table.stats tr')
    i = random.randrange(1, len(rows))
    cells = rows[i].find_all('td')
    text_id = int(re.sub(r'#(\d+)', r'\1', cells[1].get_text()))
    text = cells[2].a.get_text()
    return text_id, text


class Text(object):
    """
    Represents a TypeThief text
    Each text has set of scored characters, and the next available character
    """
    def __init__(self, text=None, encoded=None):
        """
        text [str]: base string that the text represents, will be generated if none provided
        encoded [dict]: encoded text; will override others if provided
        """
        if encoded:
            self.decode(encoded)
            return

        if not text:
            text_id, text = get_random_text()
        self._text = text
        self._characters = self._make_characters(text)
        self._next = 0

    def encode(self):
        return {
            'text': self._text,
            'next': self._next,
        }

    def decode(self, encoded):
        self._text = encoded['text']
        self._next = encoded['next']
        self._characters = self._make_characters(self._text)

    def _next_char(self):
        if self._next >= len(self._characters):
            return None
        else:
            return self._characters[self._next]

    @property
    def text(self):
        return self._text

    @property
    def next_char(self):
        return self._next_char().c

    @staticmethod
    def _make_characters(text):
        characters = []
        for i in range(len(text)):
            char = Character(i, text[i], 1)
            characters.append(char)
        return characters

    def claim_next(self, player):
        char = self._next_char()
        player.add_claimed(char)
        char.claimer = player.id
        self._next += 1


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
        self._claimer = None

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
            'claimer': self._claimer,
        }

    def decode(self, encoded):
        self._position = encoded['position']
        self._char = encoded['char']
        self._value = encoded['value']
        self._claimer = encoded['claimer']

    @property
    def pos(self):
        return self._position

    @property
    def c(self):
        return self._char

    @property
    def val(self):
        return self._value

    @property
    def claimer(self):
        return self._claimer

    @claimer.setter
    def claimer(self, new_claimer):
        self._claimer = new_claimer
