# typethief/client/__init__.py

import threading
import time

import pygame
from .button import button
from .button import room_button
from .button import text
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
        super(Client, self).__init__(server_address, server_port)

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
                background = None
                if ci < len(claimed):
                    c, val, claimer = claimed[ci]
                    ci += 1
                    #color = 255, 0, 0
                    player = self.room.get_player(claimer)
                    background = player.color

                surfrects.append(render_text(
                    lx, ly, c, font,
                    color=color, background=background,
                ))
                lx += font.size(c)[0]
            ly += font.size(l)[1]

        for surf, rect in surfrects:
            self._game_window.screen.blit(surf, rect)

    def _choose_room(self, room_id=None):
        if room_id:
            pass
        else:
            self._send_new_room()
        self._state = 'in_room'

    def _draw(self):
        button(
            680, 410, 260, 50,
            'Quit',
            (255, 0, 0), (220, 20, 60),
            self._game_window.screen,
            self._quit
        )
        
        if self._state == 'menu':

            self._send_get_rooms()
            open_rooms = self._get_open_rooms()
            self._draw_room_menu(open_rooms)

            button(
                680, 350, 260, 50,
                'New Room',
                (0, 255, 0), (50, 205, 50),
                self._game_window.screen,
                self._choose_room,
            )
            
        elif self._state == 'in_room':
            if self.room:
                font = pygame.font.SysFont('arial', 20)
                self._draw_text(20, 20, 600, font)

                if self.room.state == 'waiting':
                    button(
                        680, 280, 260, 50,
                        'Play',
                        (0, 255, 0), (50, 205, 50),
                        self._game_window.screen,
                        self._send_play,
                    )
                elif self.room.state == 'playing':
                    button( # inactive button
                        680, 280, 260, 50,
                        'Playing',
                        (144, 238, 144), (144, 238, 144),
                        self._game_window.screen,
                    )

    def _draw_room_menu(self, rooms):
            roomMenu = pygame.Surface((260, 250))
            roomMenu.fill((176, 224, 230))
            text(
                0, 0, 260, 50,
                'Get Room',
                (176, 224, 230),
                roomMenu,
            )
            y = 50
            for room in rooms:
                room_button(
                    0, y, 260, 50,
                    str(room),
                    (95, 158, 160), (176, 224, 230),
                    roomMenu,
                )
                y += 50
            
            self._game_window.screen.blit(roomMenu, (680, 30))


    def run(self):
        super(Client, self).run() # updates room
        running = True
        while running:
            try:
                self._game_window.clear_screen()

                mods = pygame.key.get_mods()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        k = to_char(event.key, shifted=bool(mods & pygame.KMOD_SHIFT))
                        if k:
                            self._send_input(k)

                self._draw()
                self._game_window.draw()
            except KeyboardInterrupt:
                running = False
        self._quit()
