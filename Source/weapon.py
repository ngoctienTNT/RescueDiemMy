''' Define weapons.
'''


from flying_object import FlyingObject


class Laser(FlyingObject):

    def _reset(self):
        if self._position == 'left':
            self.rect.left = self._plane_rect.left + 2
            self.rect.top = self._plane_rect.top - self.rect.height + 2
        if self._position == 'right':
            self.rect.left = self._plane_rect.left + self._plane_rect.width - self.rect.width - 2
            self.rect.top = self._plane_rect.top - self.rect.height + 2
        if self._position == 'center':
            self.rect.left = self._plane_rect.left + (self._plane_rect.width - self.rect.width) // 2
            self.rect.top = self._plane_rect.top - self.rect.height

    def _update_when_killed_hook(self):
        self.kill()

    def __init__(self, screen_size, image, plane_rect, plane_level, speed, damage, position, size=None):
        super().__init__(screen_size, image, size)
        self._plane_rect = plane_rect
        self._plane_level = plane_level
        self._speed = speed
        self._strike = damage
        self._position = position

        # Init.
        self._reset()


class PlayerLaser(Laser):

    def _update_when_not_killed_hook(self):
        self.rect.top -= self._speed
        if self.rect.bottom <= 0:
            self.kill()


class EnemyLaser(Laser):

    def _reset(self):
        if self._position == 'left':
            self.rect.left = self._plane_rect.left + 2
            self.rect.top = self._plane_rect.top + self.rect.height + 2
        if self._position == 'right':
            self.rect.left = self._plane_rect.left + self._plane_rect.width - self.rect.width - 2
            self.rect.top = self._plane_rect.top + self.rect.height + 2
        if self._position == 'center':
            self.rect.left = self._plane_rect.left + (self._plane_rect.width - self.rect.width) // 2
            self.rect.top = self._plane_rect.top + self.rect.height + 2

    def _update_when_not_killed_hook(self):
        self.rect.top += self._speed
        if self.rect.top > self._screen_height:
            self.kill()


class Shield(FlyingObject):

    def _update_when_not_killed_hook(self):
        self.rect.left = self._plane_rect.left - (self.rect.width - self._plane_rect.width) // 2
        self.rect.top = self._plane_rect.top - self._plane_rect.height

    def __init__(self, screen_size, image, plane_rect, size=None):
        super().__init__(screen_size, image, size)
        self._plane_rect = plane_rect
        self._strike = 500
