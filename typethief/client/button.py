# typethief/client/button.py

import pygame
from .textutils import render_text


def button(x, y, w, h, text, on_color, off_color, screen, action=None):
    dims = x, y, w, h
    mx, my = pygame.mouse.get_pos()
    ox, oy = screen.get_abs_offset()

    if x < mx - ox < x + w and y < my - oy < y + h:
        pygame.draw.rect(screen, on_color, dims)
        for e in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if e.button and action:
                action()
            pygame.event.post(e)
    else:
        pygame.draw.rect(screen, off_color, dims)

    font = pygame.font.SysFont('arial', 18)
    tw, th = font.size(text)
    surf, rect = render_text(x + (w - tw)/2, y + (h - th)/2, text, font)
    screen.blit(surf, rect)
