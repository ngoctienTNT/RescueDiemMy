''' ABC class for all sprites in this game.
'''

import pygame


class FlyingObject(pygame.sprite.Sprite):
    '''
    '''

    def _reset(self):
        self.image = self._origin_image
        self._blood = self._origin_blood
        self._killed = False

    def _update_when_not_killed_hook(self):
        pass

    def _update_when_killed_hook(self):
        pass

    def __init__(self, screen_size, image, size=None):
        super().__init__()
        self.image = image
        self._size = size
        if self._size is not None:
            self.image = pygame.transform.smoothscale(self.image, self._size)
        self.rect = self.image.get_rect()
        self._origin_image = self.image
        self._screen_width = screen_size[0]
        self._screen_height = screen_size[1]
        self._killed = False
        self._speed = 5  # May be overwritten subclass objects.
        self._blood = 1  # May be overwritten subclass objects.
        self._origin_blood = self._blood  # May be overwritten subclass objects.
        self._strike = 0  # May be overwritten subclass objects.

    def damage(self):
        return self._strike

    def lose_blood(self, damage):
        self._blood -= damage

    def get_blood(self):
        return self._blood

    def set_killed(self, v=True):
        self._killed = v

    def is_killed(self):
        return self._killed

    def update(self):
        if not self._killed:
            self._update_when_not_killed_hook()
        else:
            self._update_when_killed_hook()
