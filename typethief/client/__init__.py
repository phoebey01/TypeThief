# typethief/client/__init__.py

import threading
from queue import PriorityQueue

import pygame
from .button import button
from .gamewindow import GameWindow
from .textutils import render_lines
from .textutils import wrap_text
from typethief.shared.room import Room
from .socketclient import SocketClient


class Client(SocketClient):
    """
    Client represents the game client. It encapsulates everything about it,
    including the game window, networking, and event handling.
    """
    def __init__(self, server_address, server_port):
        super().__init__(server_address, server_port)
        self._game_window = GameWindow()
        self._mode = 'menu'

    def _quit(self):
        pygame.display.quit()
        pygame.quit()
        exit()

    def _choose_room(self, room_id=None):
        if room_id:
            pass
        else:
            self._send_new_room()
        self._mode = 'waiting'

    def _draw(self):
        button(
            680, 410, 260, 50,
            'Quit',
            (255, 0, 0), (220, 20, 60),
            self._game_window.screen,
            self._quit
        )
        
        if self._mode == 'menu':
            button(
                680, 350, 260, 50,
                'New Room',
                (0, 255, 0), (50, 205, 50),
                self._game_window.screen,
                self._choose_room,
            )
        elif self._mode == 'waiting':
            if self.room:
                font = pygame.font.SysFont('arial', 30)
                lines = wrap_text(self.room.text.text, font, 600)
                for surf, rect in render_lines(20, 20, lines, font):
                    self._game_window.screen.blit(surf, rect)
        elif self._mode == 'playing':
            pass

    def run(self):
        super().run() # updates room
        while True:
            try:
                self._game_window.clear_screen()
                for event in pygame.event.get([pygame.QUIT]):
                    self._quit()
                self._draw() # temp

                # todo:
                # get input
                # add things to draw
                #   self._game_window.screen.blit

                self._game_window.draw()
            except KeyboardInterrupt:
                break
        self._quit()
