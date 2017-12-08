# typethief/client/button.py

import os
from collections import OrderedDict

import pygame
from .textutils import render_text


class Button(object):
    """
    A rectangular button with basic hovering and action execution on clicking
    """
    def __init__(
        self, 
        x, y, w, h,
        text,
        on_color, off_color,
        font=None,
        action=None
    ):
        self._pos = x, y
        self._size = w, h
        self._text = text
        self._on = on_color
        self._off = off_color
        self._action = action
        self._enabled = True

        path = os.path.join(os.getcwd(), 'ui/fonts/raleway.ttf')
        self._font = font if font else pygame.font.Font(path, 18)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, new_pos):
        self._pos = new_pos

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    def draw(self, screen):
        x, y = self._pos
        w, h = self._size

        color = self._off
        if not self._enabled:
            r, g, b = self._off
            color = tuple(min(int(1.05 * (v + 50)), 255) for v in self._off)
        elif self.is_over(screen):
            color = self._on
        pygame.draw.rect(screen, color, self._pos + self._size)

        tw, th = self._font.size(self._text)
        s, r = render_text(x + (w - tw)/2, y + (h - th)/2, 
                            self._text, self._font)
        screen.blit(s, r)

    def is_over(self, screen):
        x, y = self._pos
        w, h = self._size
        mx, my = pygame.mouse.get_pos()
        ox, oy = screen.get_abs_offset()
        return x < mx - ox < x + w and y < my - oy < y + h

    def on_click(self):
        if self._enabled:
            self._action()


class ButtonGroup(object):
    """
    A vertical group of buttons that can be removed and added at any time
    If there are more buttons that the dimensions of the button group allow,
        users can scroll within the button group to reach clipped buttons
    """
    _SCROLL_SPEED = 5

    def __init__(self, x, y, w, h, on_color, off_color, font=None):
        self._pos = x, y
        self._size = w, h
        self._on = on_color
        self._off = off_color
        self._enabled = True

        path = os.path.join(os.getcwd(), 'ui/fonts/raleway.ttf')
        self._font = font if font else pygame.font.Font(path, 18)

        self._surf = None # set by draw
        self._next_btn = 0
        self._btns_y = 0
        self._btns = OrderedDict()

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, new_pos):
        self._pos = new_pos

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        for btn in self._btns.values():
            btn.enabled = value
        self._enabled = value

    def __iter__(self):
        for k in self._btns.keys():
            yield k

    def _button_height(self):
        return self._font.get_height() * 2

    def _total_height(self):
        return len(self._btns) * self._button_height()

    def add_button(self, text, action=None, btn_id=None):
        """
        Adds new button, returns key of the button
        """
        if btn_id in self._btns:
            return btn_id # do not change

        btn = Button(
            0, 0, self.size[0], self._button_height(), # y is set during draw
            text,
            self._on, self._off,
            font=self._font,
            action=action,
        )
        btn.enabled = self._enabled
        self._btns[btn_id if btn_id else self._next_btn] = btn
        self._next_btn += 1
        return btn_id if btn_id else self._next_btn - 1

    def remove_button(self, btn_id):
        """
        Remove button by id
        """
        del self._btns[btn_id]

    def _set_button_heights(self):
        i = 0
        for btn in self._btns.values():
            x, y = btn.pos
            btn.pos = x, i * self._button_height()
            i += 1

    def draw(self, screen):
        self._surf = screen.subsurface(*(self.pos + self.size))
        pygame.draw.rect(self._surf, self._off, (0, 0) + self.size)

        i = 0
        if self.pos[1] > self._total_height():
            self._btns_y = 0
        for btn in self._btns.values():
            x, y = btn.pos
            btn.pos = x, self._btns_y + i * self._button_height()
            btn.draw(self._surf)
            i += 1

    def is_over(self, screen):
        x, y = self._pos
        w, h = self._size
        mx, my = pygame.mouse.get_pos()
        ox, oy = screen.get_abs_offset()
        return x < mx  < x + w and y < my - oy < y + h

    def which_over(self):
        for k, btn in self._btns.items():
            if btn.is_over(self._surf):
                return k

    def on_click(self, btn_id):
        self._btns[btn_id].on_click()

    def on_scroll_up(self):
        h, ttl_hgt = self.size[1], self._total_height()
        if ttl_hgt > h and self._btns_y > h - ttl_hgt:
            self._btns_y -= ButtonGroup._SCROLL_SPEED

    def on_scroll_down(self):
        h, ttl_hgt = self.size[1], self._total_height()
        if ttl_hgt > h and self._btns_y < 0:
            self._btns_y += ButtonGroup._SCROLL_SPEED
