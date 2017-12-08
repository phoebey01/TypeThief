# typethief/client/gamewindow.py

import pygame


class GameWindow(object):
    """
    Screen to draw pygame objects on
    """
    BG_COLOR = 255, 255, 255

    def __init__(
        self,
        width=960,
        height=480,
        fps=100,
    ):
        pygame.init()

        self._size = width, height
        self._time = pygame.time.Clock()
        self._fps = fps
        self._screen = pygame.display.set_mode(self._size)
        
    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    @property
    def size(self):
        return self._size

    @property
    def screen(self):
        return self._screen

    def blit(self, *args, **kwargs):
        """
        Draw things onto the screen
        """
        self._screen.blit(*args, **kwargs)

    def clear_screen(self):
        """
        Fill the screen with pure white pixels
        Should be called at the beginning of every draw cycle
        """
        self._screen.fill(GameWindow.BG_COLOR)

    def draw(self):
        """
        Draws any shapes blit'd to the screen by updating the pygame display
        Should be called at the end of every draw cycle
        """
        self._time.tick(self._fps)
        pygame.event.pump()
        pygame.display.update()
