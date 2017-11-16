# typethief/shared/clock.py

import time


class Clock(object):
    """
    Time from a given epoch, in milliseconds
    """
    def __init__(self, epoch=None):
        self._epoch = int(epoch if epoch else time.time() * 1000)

    @property
    def epoch(self):
        return self._epoch

    @property
    def time(self):
        return int(time.time() * 1000) - self._epoch
