''' Define player plane.
'''


import os
import pygame
from pygame.locals import *
from weapon import PlayerLaser, Shield
from plane import Plane


pygame.mixer.init()
laser_sound = pygame.mixer.Sound(os.path.join('sounds', 'pew.wav'))
laser_sound.set_volume(0.2)


class Player(Plane):
    '''
    '''

    _fire_delay_factor = 4

    def _reset(self):
        super()._reset()
        # self._protected = False
        self._power = self._origin_power
        self._level = self._origin_level
        self.rect.left = (self._screen_width - self.rect.width) // 2
        self.rect.top = self._screen_height - self.rect.height

        self._protected = True
        self._activate_shield()

    def _update_when_not_killed_hook(self):
        keys_pressed = pygame.key.get_pressed()  # A list of bools of each key.
        if keys_pressed[K_UP]:
            self._move_up()
        if keys_pressed[K_DOWN]:
            self._move_down()
        if keys_pressed[K_LEFT]:
            self._move_left()
        if keys_pressed[K_RIGHT]:
            self._move_right()

        if keys_pressed[K_SPACE]:
            laser_sound.play()
            self._fire_process()

        if self._protected:
            self._activate_shield()

    def _update_when_killed_hook(self):
        self._reset()

    def _move_left(self):
        ''' Move the plane left.
        '''
        if self.rect.left > 0:
            self.rect.left -= self._speed
        else:
            self.rect.left = 0

    def _move_right(self):
        ''' Move the plane right.
        '''
        if self.rect.right < self._screen_width:
            self.rect.left += self._speed
        else:
            self.rect.left = self._screen_width - self.rect.width

    def _move_up(self):
        ''' Move the plane up.
        '''
        if self.rect.top > 0:
            self.rect.top -= self._speed
        else:
            self.rect.top = 0

    def _move_down(self):
        ''' Move the plane down.
        '''
        if self.rect.bottom < self._screen_height:
            self.rect.top += self._speed
        else:
            self.rect.top = self._screen_height - self.rect.height

    def _fire(self):
        if self._power == 0:
            self._laser_damage = 1
            self._laser_size = (12, 30)
        elif self._power == 1:
            self._laser_damage = 2
            self._laser_size = (18, 18)
        elif self._power == 2:
            self._laser_damage = 3
            self._laser_size = (15, 30)

        if self._level == 0:
            fire_positions = ['center']
        elif self._level == 1:
            fire_positions = ['left', 'right']
        elif self._level == 2:
            fire_positions = ['left', 'right', 'center']

        for i in range(self._level + 1):
            laser = PlayerLaser(
                (self._screen_width, self._screen_height),
                self._lasers[self._power],
                self.rect,
                self._level,
                self._laser_speed,
                self._laser_damage,
                fire_positions[i],
                self._laser_size
            )
            for gp in self._laser_groups:
                gp.add(laser)

    def _activate_shield(self):
        shield = Shield(
            (self._screen_width, self._screen_height),
            self._shields[0],
            self.rect,
            None
        )
        for gp in self._shield_groups:
            gp.add(shield)

    def __init__(self, screen_size, image, lasers, laser_groups, shields, shield_groups, models, size=None):
        ''' Initialize a player plane.
        '''

        super().__init__(screen_size, image, lasers, laser_groups, size)
        self._speed = 10
        self._blood = 10
        self._origin_blood = self._blood
        self._strike = 500  # Can hit any enemies except boss.
        self._power_limit = 2
        self._level_limit = 2
        self._models = [pygame.transform.smoothscale(model, size) for model in models] if size is not None else models
        self._shields = shields
        self._shield_groups = shield_groups
        self._laser_speed = 15
        self._laser_damage = 1
        self._laser_size = (9, 30)
        self._protected = False
        self._lives = 2

        # Init.
        self._reset()

    def is_protected(self):
        return self._protected

    def set_protected(self, v=True):
        self._protected = v

    def power_up(self):
        if self._power < self._power_limit:
            self._power += 1

    def level_up(self):
        if self._level < self._level_limit:
            self._level += 1
        self.image = self._models[self._level]
        self._blood = self._origin_blood

    def blood_up(self):
        self._blood += 3
        if self._blood > self._origin_blood:
            self._blood = self._origin_blood

    def get_lives(self):
        return self._lives

    def lose_lives(self, v=1):
        self._lives -= v
