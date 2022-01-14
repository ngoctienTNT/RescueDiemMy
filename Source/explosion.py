''' Define Explosion Class.
'''

import pygame
from flying_object import FlyingObject


class Explosion(FlyingObject):

    def _update_when_killed_hook(self):
        self.kill()

    def _update_when_not_killed_hook(self):
        self.image = self._frames[self._i]
        if self._size is not None:
            self.image = pygame.transform.smoothscale(self.image, self._size)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        self._i += 1
        if self._i >= len(self._frames):
            self._killed = True
            self._i = 0

    def __init__(self, screen_size, image, center, frames, size=None):
        super().__init__(screen_size, image, size)
        self.rect.center = center
        self._frames = frames
        self._i = 0
