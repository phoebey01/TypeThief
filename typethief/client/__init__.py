# typethief/client/__init__.py

import threading
import time
import os

import pygame
from .button import Button
from .button import ButtonGroup
from .gamewindow import GameWindow
from .textutils import to_char
from .textutils import rect_text
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

        # buttons
        self._quit_btn = Button(
            680, 410, 260, 50,
            'Quit',
            (255, 0, 0), (220, 20, 60),
            action=self._quit,
        )
        self._new_room_btn = Button(
            680, 345, 260, 50,
            'New Room',
            (0, 255, 0), (50, 205, 50),
            action=self._choose_room,
        )
        self._play_btn = Button(
            680, 280, 260, 50,
            'Play',
            (0, 255, 0), (50, 205, 50),
            action=self._send_play,
        )
        self._leave_room_btn = Button(
            680, 345, 260, 50,
            'Leave Room',
            (230, 153, 255), (204, 153, 255),
            action=self._leave_room,
        )
        self._btns = set([
            self._quit_btn,
            self._new_room_btn,
            self._play_btn,
            self._leave_room_btn,
        ])

        # room selector
        self._rooms_group = ButtonGroup(
            680, 70, 260, 260,
            (95, 158, 160), (176, 224, 230),
        )

    def _quit(self):
        self._leave_room()
        pygame.display.quit()
        pygame.quit()
        exit()

    def _draw_text(self, x, y, w, font):
        text_obj = self.room.text
        text = text_obj.text
        if text_obj.next_pos is not None:
            claimed = [text_obj.get_char(i) for i in range(text_obj.next_pos)]
        else: 
            claimed = []
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
                    player = self.room.get_player(claimer)
                    background = player.color if player else None
                    color = (0, 0, 0) if player else (255, 0, 0)

                surfrects.append(render_text(
                    lx, ly, c, font,
                    color=color, background=background,
                ))
                lx += font.size(c)[0]
            ly += font.size(l)[1]

        for surf, rect in surfrects:
            self._game_window.blit(surf, rect)

    def _choose_room(self, room_id=None):
        if room_id:
            self._send_join_room(room_id)
        else:
            self._send_new_room()
        self._state = 'in_room' # todo: fix if unsuccessful room join

    def _leave_room(self):
        if self.room:
            self._send_leave_room()
        self._state = 'menu'

    def _draw_room_menu(self, rooms):
        screen = self._game_window.screen
        rect_text(680, 20, 260, 50, 'Open Rooms', (65, 105, 225), screen)
        self._rooms_group.draw(screen)

        dead_btns = [btn_id for btn_id in self._rooms_group if btn_id not in rooms]
        for btn_id in dead_btns:
            self._rooms_group.remove_button(btn_id)
        new_btns = [rid for rid in rooms if rid not in self._rooms_group]
        for btn_id in new_btns:
            self._rooms_group.add_button(
                str(btn_id),
                action=lambda: self._choose_room(room_id=btn_id),
                btn_id=btn_id,
            )

    def _draw_player_panel(self):
        x, y = 680, 20
        pygame.draw.rect(
            self._game_window.screen, 
            (220, 220, 220),
            (x, y, 260, 240),
        )
        rect_text(
            x, y, 260, 30,
            "Players",
            (128, 128, 128),
            self._game_window.screen,
        )

        font_hgt = 12
        def draw_player_info(x, y, name, color, score):
            font = pygame.font.SysFont('arial', font_hgt)
            lsurf, lrect = render_text(x, y, name + ' ', font)
            self._game_window.blit(lsurf, lrect)
            mrect = pygame.draw.rect(
                self._game_window.screen,
                color,
                (lrect.right, y, lrect.height, lrect.height),
            )
            rsurf, rrect = render_text(mrect.right, y, ': {}'.format(score), font)
            self._game_window.blit(rsurf, rrect)

        px, py = x + 10, y + 40

        # current player
        curr = self.room.get_player(self.player_id)
        draw_player_info(px, py, "You", curr.color, curr.score)
        py += font_hgt * 2

        # other players
        i = 0
        for p in self.room:
            if not p:
                continue
            elif p.id != curr.id:
                draw_player_info(px, py, "Player{}".format(i), p.color, p.score)
                py += font_hgt
            i += 1

    def _draw_logo(self):
        asurf = pygame.image.load(os.path.join(os.getcwd(),'ui/img/logo6.png'))
        asurf = pygame.transform.scale(asurf, (300, 300))
        arect = asurf.get_rect()
        arect.center = (300,240)
        self._game_window.blit(asurf, arect)

    def _draw(self):
        screen = self._game_window.screen
        pygame.draw.rect(screen, (0, 0, 0), (660, 0, 300, 480))
        self._quit_btn.draw(screen)

        # set btn states
        self._rooms_group.enabled = not self.room
        self._new_room_btn.enabled = not self.room
        self._play_btn.enabled = self.room and self.room.state == 'waiting'
        self._leave_room_btn.enabled = self.room and self.room.state != 'playing'
        
        if self._state == 'menu':
            self._send_get_rooms()
            open_rooms = self._get_open_rooms()
            self._draw_room_menu(open_rooms)
            self._new_room_btn.draw(screen)
            self._draw_logo()
            
        elif self._state == 'in_room':
            self._leave_room_btn.draw(screen)

            if self.room and self.room.state != 'finished':
                font = pygame.font.SysFont('arial', 20)
                # mac font adjustment
                w, h = pygame.display.get_surface().get_size()
                if w == 960 and h == 480:
                    path = os.path.join(os.getcwd(), 'ui/fonts/raleway.ttf')
                    font = pygame.font.Font(path, 25)
                self._draw_text(20, 20, 600, font)
                self._draw_player_panel()
                self._play_btn.draw(screen)

            elif self.room and self.room.state == 'finished':
                path = os.path.join(os.getcwd(), 'ui/fonts/win.otf')
                font = pygame.font.Font(path, 60)
                self.room.compute_winner()
                color = (255, 128, 0) if self.room.winner.id == self.player_id else (191, 255, 0)
                result_msg = 'YOU WIN!' if self.room.winner.id == self.player_id else 'YOU LOSE!'
                surf, rect = render_text(200, 200, result_msg, font, color)
                self._game_window.blit(surf, rect)
                    

    def run(self):
        super(Client, self).run() # updates room
        screen = self._game_window.screen
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
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            room_btn = self._rooms_group.which_over()
                            if room_btn:
                                self._rooms_group.on_click(room_btn)
                            for btn in self._btns:
                                if btn.is_over(screen):
                                    btn.on_click()
                        elif event.button == 4:
                            if self._rooms_group.is_over(screen):
                                self._rooms_group.on_scroll_up()
                        elif event.button == 5:
                            if self._rooms_group.is_over(screen):
                                self._rooms_group.on_scroll_down()

                self._draw()
                self._game_window.draw()
            except KeyboardInterrupt:
                running = False
        self._quit()
