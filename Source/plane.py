''' Define ABC Plane class for Player and Enemy.
'''

from flying_object import FlyingObject


class Plane(FlyingObject):

    _fire_delay_factor = 50  # May be overwritten subclass objects.

    def _fire_process(self):
        if not (self._fire_delay % self._fire_delay_factor):
            self._fire()
        self._fire_delay -= 1
        if self._fire_delay <= 0:
            self._fire_delay = 500

    def _fire(self):
        raise NotImplementedError('Plz define _fire in subclass')

    def __init__(self, screen_size, image, lasers, laser_groups, size=None):
        super().__init__(screen_size, image, size)
        self._power = 0  # May be overwritten subclass objects.
        self._level = 0  # May be overwritten subclass objects.
        self._origin_level = self._level  # May be overwritten subclass objects.
        self._origin_power = self._power  # May be overwritten subclass objects.
        self._lasers = lasers
        self._laser_groups = laser_groups
        self._laser_speed = 15
        self._laser_damage = 1
        self._laser_size = (9, 30)
        self._fire_delay = 500  # May be overwritten subclass objects.
