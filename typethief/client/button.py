# typethief/client/button.py

import pygame
from .textutils import render_text


def button(x, y, w, h, text, on_color, off_color, screen, action=None):
    dims = x, y, w, h
    mx, my = pygame.mouse.get_pos()
    mdown, mup, mmotion = pygame.mouse.get_pressed()

    if x < mx < x + w and y < my < y + h:
        pygame.draw.rect(screen, on_color, dims)
        if mdown and action:
            action()
    else:
        pygame.draw.rect(screen, off_color, dims)

    font = pygame.font.SysFont('arial', 18)
    tw, th = font.size(text)
    surf, rect = render_text(x + (w - tw)/2, y + (h - th)/2, text, font)
    screen.blit(surf, rect)

def room_button(x, y, w, h, text, on_color, off_color, screen, action=None):
    dims = x, y, w, h
    mx, my = pygame.mouse.get_pos()
    mdown, mup, mmotion = pygame.mouse.get_pressed()
    buffer_left = 680
    buffer_top = 30

    if buffer_left+x < mx < buffer_left+x + w and buffer_top + y < my < buffer_top + y + h:
        pygame.draw.rect(screen, on_color, dims)
        if mdown and action:
            action()
    else:
        pygame.draw.rect(screen, off_color, dims)

    font = pygame.font.SysFont('arial', 18)
    tw, th = font.size(text)
    surf, rect = render_text(x + (w - tw)/2, y + (h - th)/2, text, font)
    screen.blit(surf, rect)