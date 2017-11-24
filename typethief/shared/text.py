# typethief/shared/text.py

import os
import json
import random
import re
import requests
import threading

from bs4 import BeautifulSoup


_TYPERACER_TEXTS_URL = 'http://www.typeracerdata.com/texts?texts=full&sort=relative_average'
_TEXTS_FNAME = 'typethief/shared/texts.txt'


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


class Text(object):
    """
    Represents a TypeThief text
    Each text has set of scored characters, and the next available character
    """
    _cached_texts = {}

    def __init__(self, text=None, encoded=None):
        """
        text [str]: base string that the text represents, will be generated if none provided
        encoded [dict]: encoded text; will override others if provided
        """
        self._claim_mutex = threading.Lock()

        if encoded:
            self.decode(encoded)
            return

        if not text:
            text_id, text = Text._get_random_text()
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

    @property
    def next_pos(self):
        return self._next

    def get_char(self, i):
        """
        Returns char of the form:
        (character, value, claimer)
        """
        char = self._characters[i]
        return char.c, char.val, char.claimer

    @classmethod
    def _get_random_text(cls):
        """
        Lazily loads texts to cls._cached_texts
        Texts are scraped from TypeRacer
        Loaded from file if available
        """
        if not cls._cached_texts:
            if os.path.isfile(_TEXTS_FNAME):
                with open(_TEXTS_FNAME, 'r') as f:
                    cls._cached_texts = json.load(f)
            else:
                r = requests.get(_TYPERACER_TEXTS_URL)
                soup = BeautifulSoup(r.text, 'html.parser')
                rows = soup.select('table.stats tr')
                for i in range(1, len(rows)):
                    cells = rows[i].find_all('td')
                    text_id = int(re.sub(r'#(\d+)', r'\1', cells[1].get_text()))
                    text = cells[2].a.get_text()
                    cls._cached_texts[text_id] = text

                # save texts to file
                with open(_TEXTS_FNAME, 'w+') as f:
                    json.dump(cls._cached_texts, f)

        text_id, text = random.choice(cls._cached_texts.items())
        return text_id, text

    @staticmethod
    def _make_characters(text):
        characters = []
        for i in range(len(text)):
            char = Character(i, text[i], 1)
            characters.append(char)
        return characters

    def _claim_pos(self, player, pos):
        pos_char = self._characters[pos] # can raise index
        if not pos_char.claimer:
            player.add_claimed(pos_char)
            pos_char.claimer = player.id

    def claim_pos(self, player, pos):
        with self._claim_mutex:
            self._claim_pos(player, pos)

    def claim_next(self, player, char=None):
        """
        Returns index of claimed character if successful, None otherwise
        """
        with self._claim_mutex:
            if not char or (self._next_char() and char == self._next_char().c):
                self._claim_pos(player, self._next)
                claimed = self._next
                self._next += 1
                return claimed
        return None
