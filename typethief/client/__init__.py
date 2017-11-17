# typethief/client/__init__.py

import threading
from queue import PriorityQueue

import pygame
from .button import button
from .gamewindow import GameWindow
from .textutils import to_char
from .textutils import render_text
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
        self._state = 'menu' # menu, waiting, playing

    def _quit(self):
        pygame.display.quit()
        pygame.quit()
        exit()

    def _draw_text(self, x, y, w, font):
        text_obj = self.room.text
        text = text_obj.text
        claimed = [text_obj.get_char(i) for i in range(text_obj.next_pos)]
        lines = wrap_text(text, font, w)

        # draw lines before next_line
        surfrects = []
        ci, ly = 0, y

        for l in lines:
            lx = x
            for c in l:
                color = 0, 0, 0
                if ci < len(claimed):
                    c, val, claimer = claimed[ci]
                    ci += 1
                    color = 255, 0, 0
                surfrects.append(render_text(lx, ly, c, font, color=color))
                lx += font.size(c)[0]
            ly += font.size(l)[1]

        for surf, rect in surfrects:
            self._game_window.screen.blit(surf, rect)

    def _choose_room(self, room_id=None):
        if room_id:
            pass
        else:
            self._send_new_room()
        self._state = 'waiting'

    def _draw(self):
        button(
            680, 410, 260, 50,
            'Quit',
            (255, 0, 0), (220, 20, 60),
            self._game_window.screen,
            self._quit
        )
        
        if self._state == 'menu':
            button(
                680, 350, 260, 50,
                'New Room',
                (0, 255, 0), (50, 205, 50),
                self._game_window.screen,
                self._choose_room,
            )
        elif self._state == 'waiting':
            if self.room:
                font = pygame.font.SysFont('arial', 20)
                self._draw_text(20, 20, 600, font)
        elif self._state == 'playing':
            pass

    def run(self):
        super().run() # updates room
        running = True
        while running:
            try:
                self._game_window.clear_screen()

                mods = pygame.key.get_mods()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif self.event.type == pygame.KEYDOWN:
                        k = to_char(event.key, shifted=bool(mods & pygame.KMOD_SHIFT))
                        self._send_input(k)

                self._draw() # temp

                # todo:
                # get input
                # add things to draw
                #   self._game_window.screen.blit

                self._game_window.draw()
            except KeyboardInterrupt:
                running = False
        self._quit()
