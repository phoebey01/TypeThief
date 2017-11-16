# typethief/client/button.py

import pygame


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
    surf = font.render(text, True, (0, 0, 0))
    rect = surf.get_rect()
    rect.center = x + w/2, y + h/2
    screen.blit(surf, rect)
