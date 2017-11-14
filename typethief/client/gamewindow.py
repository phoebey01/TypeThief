# typethief/client/gamewindow.py

import pygame


class GameWindow(object):
    """
    """
    BG_COLOR = 255, 255, 255
    MODES = ['MENU', 'WAITING', 'PLAYING']

    def __init__(
        self,
        width=960,
        height=480,
        fps=100,
    ):
        pygame.init()

        self.size = width, height
        self.mode = 'PLAYING' # todo: after making menu, switch

        self.time = pygame.time.Clock()
        self.fps = fps

        self.screen = pygame.display.set_mode(self.size)

    def draw(self):
        self.screen.fill(GameWindow.BG_COLOR)
        # todo: draw screen based on mode
        pygame.display.update()

    def run(self):
        while True:
            self.time.tick(self.fps)
            self.draw()
