# typethief/client/__init__.py

import threading
from queue import PriorityQueue

import pygame
from .gamewindow import GameWindow
from typethief.shared.room import Room
from .socketclient import SocketClient


class Client(object):
    """
    Client represents the game client. It encapsulates everything about it,
    including the game window, networking, and event handling.
    """
    def __init__(self, server_address, server_port):
        self._socket_client = SocketClient(server_address, server_port)
        self._game_window = GameWindow()

    def run(self):
        self._socket_client.run() # updates room
        while True:
            try:
                self._game_window.clear_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.display.quit()
                        pygame.quit()
                        exit()
                # get input
                # add things to draw
                #   self._game_window.screen.blit
                self._game_window.draw()
            except KeyboardInterrupt:
                break
        exit()
