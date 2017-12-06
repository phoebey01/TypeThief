# typethief/client/button.py
import os
import pygame
from .textutils import render_text


def button(x, y, w, h, text, on_color, off_color, screen, action=None):
    dims = x, y, w, h
    mx, my = pygame.mouse.get_pos()
    ox, oy = screen.get_abs_offset()
    mdown, mup, mmotion = pygame.mouse.get_pressed()

    if x < mx - ox < x + w and y < my - oy < y + h:
        pygame.draw.rect(screen, on_color, dims)
        if mdown and action:
            action()
    else:
        pygame.draw.rect(screen, off_color, dims)

    # font = pygame.font.SysFont('arial', 18)
    path = os.path.join(os.getcwd(), 'ui/fonts/raleway.ttf')
    font = pygame.font.Font(path, 18)
    tw, th = font.size(text)
    surf, rect = render_text(x + (w - tw)/2, y + (h - th)/2, text, font)
    screen.blit(surf, rect)
