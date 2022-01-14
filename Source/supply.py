''' Define supplies.
'''

from flying_object import FlyingObject
from random import randint


class Supply(FlyingObject):

    def _reset(self):
        super()._reset()
        self.rect.left = randint(0, self._screen_width - self.rect.width)
        self.rect.top = randint(-10 * self.rect.height, -self.rect.height)

    def _update_when_not_killed_hook(self):
        self.rect.top += self._speed
        if self.rect.top >= self._screen_height:
            self._reset()
            self.kill()

    def _update_when_killed_hook(self):
        self._reset()
        self.kill()
        # pass

    def __init__(self, screen_size, image, size=None):
        super().__init__(screen_size, image, size)

        # Init.
        self._reset()
