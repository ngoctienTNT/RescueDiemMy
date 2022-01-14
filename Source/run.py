''' A plane wars game demo.

'''

import sys
import os
import pygame
from pygame.locals import *
from player_plane import Player
from enemy_plane import ElementaryEnemy, MidEnemy, AdvancedEnemy, Meteor
from supply import Supply
from explosion import Explosion
from mygroup import ContainerGroup
from random import choice

# ------------------------- Initialize game -------------------------
pygame.init()
width = 600
height = 800 if pygame.display.Info().current_h >= 900 else pygame.display.Info().current_h - 100
screen_size = width, height  # Screen size.
screen = pygame.display.set_mode(screen_size)  # Screen.
pygame.display.set_caption('Plane War Demo')  # Caption.
clock = pygame.time.Clock()  # Clock.

# ------------------------- Set colors -------------------------
GREEN = (14, 242, 44)
WHITE = (255, 255, 255)

# ------------------------- Set image dirs and loaded images -------------------------
BACKGROUND_DIR = os.path.join('images', 'backgrounds')
ENEMY_DIR = os.path.join('images', 'enemies')
EXPLOSION_DIR = os.path.join('images', 'explosions')
MENU_DIR = os.path.join('images', 'menu')
PLAYER_DIR = os.path.join('images', 'players')
SUPPLY_DIR = os.path.join('images', 'supplies')
WEAPON_DIR = os.path.join('images', 'weapons')

IMAGES = {
    'backgrounds': [
        pygame.image.load(BACKGROUND_DIR + '/starfield.png').convert_alpha(),
    ],
    'elementary_enemies': [
        pygame.image.load(ENEMY_DIR + '/enemyBlue3.png').convert_alpha(),
    ],
    'mid_enemies': [
        pygame.image.load(ENEMY_DIR + '/enemyBlue4.png').convert_alpha(),
    ],
    'advanced_enemies': [
        pygame.image.load(ENEMY_DIR + '/ufoBlue.png').convert_alpha(),
    ],
    'tiny_meteors': [
        pygame.image.load(ENEMY_DIR + '/meteorBrown_tiny2.png').convert_alpha(),
    ],
    'small_meteors': [
        pygame.image.load(ENEMY_DIR + '/meteorBrown_small2.png').convert_alpha(),
    ],
    'med_meteors': [
        pygame.image.load(ENEMY_DIR + '/meteorBrown_med3.png').convert_alpha(),
    ],
    'big_meteors': [
        pygame.image.load(ENEMY_DIR + '/meteorBrown_big2.png').convert_alpha(),
    ],
    'menu': [
        pygame.image.load(MENU_DIR + '/main.png').convert_alpha(),
    ],
    'enemy_explosions': [
        pygame.image.load(EXPLOSION_DIR + '/regularExplosion00.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/regularExplosion01.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/regularExplosion02.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/regularExplosion03.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/regularExplosion04.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/regularExplosion05.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/regularExplosion06.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/regularExplosion07.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/regularExplosion08.png').convert_alpha(),
    ],
    'player_explosions': [
        pygame.image.load(EXPLOSION_DIR + '/sonicExplosion00.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/sonicExplosion01.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/sonicExplosion02.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/sonicExplosion03.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/sonicExplosion04.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/sonicExplosion05.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/sonicExplosion06.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/sonicExplosion07.png').convert_alpha(),
        pygame.image.load(EXPLOSION_DIR + '/sonicExplosion08.png').convert_alpha(),
    ],
    'players': [
        pygame.image.load(PLAYER_DIR + '/playerShip1_red.png').convert_alpha(),
        pygame.image.load(PLAYER_DIR + '/playerShip2_red.png').convert_alpha(),
        pygame.image.load(PLAYER_DIR + '/playerShip3_red.png').convert_alpha(),
    ],
    'player_lifes': [
        pygame.image.load(PLAYER_DIR + '/playerLife1_red.png').convert_alpha(),
    ],
    'player_lasers': [
        pygame.image.load(WEAPON_DIR + '/laserRed01.png').convert_alpha(),
        pygame.image.load(WEAPON_DIR + '/laserRed09.png').convert_alpha(),
        pygame.image.load(WEAPON_DIR + '/laserRed04.png').convert_alpha(),
    ],
    'player_lasers_shot': [
        pygame.image.load(WEAPON_DIR + '/laserRedShot.png').convert_alpha(),
    ],
    'elementary_enemy_lasers': [
        pygame.image.load(WEAPON_DIR + '/laserBlue09.png').convert_alpha(),
    ],
    'mid_enemy_lasers': [
        pygame.image.load(WEAPON_DIR + '/laserBlue13.png').convert_alpha(),
    ],
    'advanced_enemy_lasers': [
        pygame.image.load(WEAPON_DIR + '/laserBlue15.png').convert_alpha(),
    ],
    'enemy_lasers_shot': [
        pygame.image.load(WEAPON_DIR + '/laserBlueShot.png').convert_alpha(),
    ],
    'protections': [
        pygame.image.load(WEAPON_DIR + '/shield3.png').convert_alpha(),
    ],
    'shields': [
        pygame.image.load(SUPPLY_DIR + '/shield_gold.png').convert_alpha(),
    ],
    'powerups': [
        pygame.image.load(SUPPLY_DIR + '/bolt_gold.png').convert_alpha(),
    ],
    'stars': [
        pygame.image.load(SUPPLY_DIR + '/star_gold.png').convert_alpha(),
    ],
    'pills': [
        pygame.image.load(SUPPLY_DIR + '/pill_green.png').convert_alpha(),
    ],
}

# ------------------------- Set sounds -------------------------
menu_sound = pygame.mixer.Sound(os.path.join('sounds', 'menu.ogg'))
main_sound = pygame.mixer.Sound(os.path.join('sounds', 'game_seamlessloop.ogg'))
main_sound.set_volume(0.4)
shieldup_sound = pygame.mixer.Sound(os.path.join('sounds', 'sfx_shieldUp.ogg'))
shielddown_sound = pygame.mixer.Sound(os.path.join('sounds', 'sfx_shieldDown.ogg'))
enemy_explo_sounds = [
    pygame.mixer.Sound(os.path.join('sounds', 'expl3.wav')),
    pygame.mixer.Sound(os.path.join('sounds', 'expl6.wav')),
]
player_explo_sound = pygame.mixer.Sound(os.path.join('sounds', 'rumble1.ogg'))

# ------------------------- Set sizes -------------------------
background_size = background_width, background_height = width, height
blood_strip_size = blood_strip_width, blood_strip_height = 3, 15
blood_strip_gap = 10
player_life_gap = 10
player_size = (90, 90)
elementary_enemy_size = (122, 80)
mid_enemy_size = (55, 50)
advanced_enemy_size = (60, 60)
bolt_size = (20, 32)
star_size = pill_size = shield_size = (30, 30)
player_laser_shot_size = (40, 40)
enemy_laser_shot_size = (20, 20)

# ------------------------- Set fps -------------------------
fps = 60

# ------------------------- Set font -------------------------
font_file = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_file, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_menu():
    global screen

    menu_sound.play(-1)

    menu = IMAGES['menu'][0]
    menu = pygame.transform.smoothscale(menu, screen_size)

    while True:
        clock.tick(fps)

        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                menu_sound.stop()
                return True
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

        screen.blit(menu, (0, 0))
        draw_text(screen, 'Press [ENTER] To Begin', 30, width // 2, height // 2)
        draw_text(screen, 'or [ESC] To Quit', 30, width // 2, (height // 2) + 40)

        pygame.display.flip()


def draw_exit(score):
    global screen

    menu = IMAGES['menu'][0]
    menu = pygame.transform.smoothscale(menu, screen_size)

    while True:
        clock.tick(fps)

        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

        screen.blit(menu, (0, 0))
        draw_text(screen, 'Your score: ' + str(score), 30, width // 2, height // 2)
        draw_text(screen, 'Press [ENTER] To Retry', 30, width // 2, height // 2 + 40)
        draw_text(screen, 'or [ESC] To Quit', 30, width // 2, (height // 2) + 40 * 2)

        pygame.display.flip()


def draw_backgrounds(background, background_y):
    global screen

    rel_background_y = -(background_y % background.get_rect().height)
    screen.blit(background, (0, rel_background_y + background.get_rect().height))
    screen.blit(background, (0, rel_background_y))
    background_y -= 1
    if background_y == -background.get_rect().height:
        background_y = 0
    return background_y


def create_sprites(num, groups, cls, *args):
    for i in range(num):
        sprite = cls(*args)
        sprite.add(*groups)
    for gp in groups:
        if hasattr(gp, 'store_permanent'):
            gp.store_permanent()


def add_sprites_from_container(container, groups):
    for sprite in container.iter_store():
        sprite.add(*groups)


def manage_sprites_with_time(tt, starts, ends, container, groups):
    for start, end in zip(starts, ends):
        if start < tt <= end:
            add_sprites_from_container(
                container,
                groups
            )


def main():

    # Global vars.
    global screen

    run = True
    first = True

    while run:

        # Configs.
        n_players = 1
        n_elementary_enemies = 4
        n_mid_enemies = 3
        n_advanced_enemies = 4
        n_tiny_meteors = 3
        n_small_meteors = 3 
        n_med_meteors = 3
        n_big_meteors = 3
        n_stars = n_pills = n_shields = n_bolts = 1
        score = 0
        shield_timer = 4  # The time limit for shielding is 4 seconds.
        tt = 0  # Total time.

        # Create groups to control when each sprite shows up.
        meteor_small_list = ContainerGroup()
        meteor_except_small_list = ContainerGroup()
        elementary_enemy_list = ContainerGroup()
        mid_enemy_list = ContainerGroup()
        advanced_enemy_list = ContainerGroup()
        star_list = ContainerGroup()
        pill_list = ContainerGroup()
        bolt_list = ContainerGroup()
        shield_list = ContainerGroup()

        # Create groups.
        all_collided_objects_g = pygame.sprite.Group()

        players_g = pygame.sprite.GroupSingle()
        protection_g = pygame.sprite.GroupSingle()

        enemies_g = pygame.sprite.Group()

        supplies_g = pygame.sprite.Group()
        pills_g = pygame.sprite.Group()
        stars_g = pygame.sprite.Group()
        shields_g = pygame.sprite.Group()
        bolts_g = pygame.sprite.Group()

        lasers_g = pygame.sprite.Group()
        player_lasers_g = pygame.sprite.Group()
        enemy_lasers_g = pygame.sprite.Group()

        explosions_g = pygame.sprite.Group()

        # Create background 'Surface'.
        background_y = 0
        background = pygame.transform.smoothscale(IMAGES['backgrounds'][0], background_size)

        # Create player life 'Surface'.
        player_life = IMAGES['player_lifes'][0]

        # Create player.
        player_args = (
            screen_size,
            IMAGES['players'][0],
            IMAGES['player_lasers'],
            (player_lasers_g, lasers_g),
            IMAGES['protections'],
            (protection_g,),
            IMAGES['players'],
            player_size,
        )
        create_sprites(n_players, (players_g,), Player, *player_args)
        player = players_g.sprite

        # Create enemies.
        elementary_enemy_args = (
            screen_size,
            IMAGES['elementary_enemies'][0],
            IMAGES['elementary_enemy_lasers'],
            (enemy_lasers_g, lasers_g),
            elementary_enemy_size,
        )
        mid_enemy_args = (
            screen_size,
            IMAGES['mid_enemies'][0],
            IMAGES['mid_enemy_lasers'],
            (enemy_lasers_g, lasers_g),
            mid_enemy_size,
        )
        advanced_enemy_args = (
            screen_size,
            IMAGES['advanced_enemies'][0],
            IMAGES['advanced_enemy_lasers'],
            (enemy_lasers_g, lasers_g),
            advanced_enemy_size,
        )
        tiny_meteor_args = (
            screen_size,
            IMAGES['tiny_meteors'][0],
            [],
            (),
            None,
        )
        small_meteor_args = (
            screen_size,
            IMAGES['small_meteors'][0],
            [],
            (),
            None,
        )
        med_meteor_args = (
            screen_size,
            IMAGES['med_meteors'][0],
            [],
            (),
            None,
        )
        big_meteor_args = (
            screen_size,
            IMAGES['big_meteors'][0],
            [],
            (),
            None,
        )
        create_sprites(
            n_elementary_enemies,
            (elementary_enemy_list,),
            ElementaryEnemy,
            *elementary_enemy_args,
        )
        create_sprites(
            n_mid_enemies,
            (mid_enemy_list,),
            MidEnemy,
            *mid_enemy_args,
        )
        create_sprites(
            n_advanced_enemies,
            (advanced_enemy_list,),
            AdvancedEnemy,
            *advanced_enemy_args,
        )
        create_sprites(
            n_tiny_meteors,
            (meteor_except_small_list,),
            Meteor,
            *tiny_meteor_args,
        )
        create_sprites(
            n_small_meteors,
            (meteor_small_list,),
            Meteor,
            *small_meteor_args,
        )
        create_sprites(
            n_med_meteors,
            (meteor_except_small_list,),
            Meteor,
            *med_meteor_args,
        )
        create_sprites(
            n_big_meteors,
            (meteor_except_small_list,),
            Meteor,
            *big_meteor_args,
        )

        # Create supplies.
        star_args = (screen_size, IMAGES['stars'][0], star_size)
        bolt_args = (screen_size, IMAGES['powerups'][0], bolt_size)
        shield_args = (screen_size, IMAGES['shields'][0], shield_size)
        pill_args = (screen_size, IMAGES['pills'][0], pill_size)
        create_sprites(
            n_stars,
            (star_list,),
            Supply,
            *star_args,
        )
        create_sprites(
            n_bolts,
            (bolt_list,),
            Supply,
            *bolt_args,
        )
        create_sprites(
            n_shields,
            (shield_list,),
            Supply,
            *shield_args,
        )
        create_sprites(
            n_pills,
            (pill_list,),
            Supply,
            *pill_args,
        )

        # Draw entry menu.
        if first:
            run = draw_menu()
            first = False

        main_sound.play(-1)

        while run:
            dt = clock.tick(fps) / 1000  # Delta time between current and last tick.
            tt += dt
            # print(tt)

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            # Draw moving background.
            background_y = draw_backgrounds(background, background_y)

            # Check collision.
            # Check collision between player and other objects.
            collides = pygame.sprite.spritecollide(player, all_collided_objects_g, False)
            player_strike_damage = player.damage()
            for colli in collides:
                colli.lose_blood(player_strike_damage)
                if colli.get_blood() <= 0:
                    colli.set_killed()

                if colli in bolts_g:
                    player.power_up()
                elif colli in stars_g:
                    player.level_up()
                elif colli in pills_g:
                    player.blood_up()
                elif colli in shields_g:
                    shieldup_sound.play()
                    player.set_protected()
                    shield_timer = 4
                elif colli in enemies_g:
                    enemy_strike_damage = colli.damage()
                    player.lose_blood(enemy_strike_damage)

            # Check collision between player lasers and enemies.
            for enemy in enemies_g:
                player_hits = pygame.sprite.spritecollide(enemy, player_lasers_g, False)
                damages = 0
                for hit in player_hits:
                    hit.lose_blood(1)
                    damages += hit.damage()
                    if hit.get_blood() <= 0:
                        hit.set_killed()
                        player_lasers_explo_args = (
                            screen_size,
                            IMAGES['player_lasers_shot'][0],
                            hit.rect.center,
                            IMAGES['player_lasers_shot'],
                            player_laser_shot_size,
                        )
                        create_sprites(
                            1,
                            (explosions_g,),
                            Explosion,
                            *player_lasers_explo_args,
                        )
                enemy.lose_blood(damages)

            # Check collision between enemy laser and player...
            enemy_hits = pygame.sprite.spritecollide(player, enemy_lasers_g, False)
            damages = 0
            for hit in enemy_hits:
                hit.lose_blood(1)
                damages += hit.damage()
                if hit.get_blood() <= 0:
                    hit.set_killed()
                    enemy_lasers_explo_args = (
                        screen_size,
                        IMAGES['enemy_lasers_shot'][0],
                        hit.rect.center,
                        IMAGES['enemy_lasers_shot'],
                        enemy_laser_shot_size,
                    )
                    create_sprites(
                        1,
                        (explosions_g,),
                        Explosion,
                        *enemy_lasers_explo_args,
                    )
            player.lose_blood(damages)

            # Check collision between enemy laser and protection shield.
            if player.is_protected() and protection_g:
                enemy_hits = pygame.sprite.spritecollide(protection_g.sprite, enemy_lasers_g, False)
                for hit in enemy_hits:
                    hit.lose_blood(1)
                    if hit.get_blood() <= 0:
                        hit.set_killed()
                        enemy_lasers_explo_args = (
                            screen_size,
                            IMAGES['enemy_lasers_shot'][0],
                            hit.rect.center,
                            IMAGES['enemy_lasers_shot'],
                            enemy_laser_shot_size,
                        )
                        create_sprites(
                            1,
                            (explosions_g,),
                            Explosion,
                            *enemy_lasers_explo_args,
                        )

                # Check collision between enemies and shield...
                enemies = pygame.sprite.spritecollide(protection_g.sprite, enemies_g, False)
                for enemy in enemies:
                    enemy.lose_blood(protection_g.sprite.damage())

                # Counting down time limit for shielding.
                shield_timer -= dt
                if shield_timer <= 0:
                    player.set_protected(False)
                    protection_g.empty()
                    shield_timer = 4
                    shielddown_sound.play()

            # Determine if player and enemy shall be explosions.
            if player.get_blood() <= 0:
                player.set_killed()
                player_explo_sound.play()
                player.lose_lives()
                player_explo_args = (
                    screen_size,
                    IMAGES['player_explosions'][0],
                    player.rect.center,
                    IMAGES['player_explosions'],
                    None,
                )
                create_sprites(
                    1,
                    (explosions_g,),
                    Explosion,
                    *player_explo_args,
                )
            for enemy in enemies_g:
                if enemy.get_blood() <= 0:
                    enemy.set_killed()
                    choice(enemy_explo_sounds).play()
                    enemy_explo_args = (
                        screen_size,
                        IMAGES['enemy_explosions'][0],
                        enemy.rect.center,
                        IMAGES['enemy_explosions'],
                        None,
                    )
                    create_sprites(
                        1,
                        (explosions_g,),
                        Explosion,
                        *enemy_explo_args,
                    )

            # Draw score.
            score += sum(enemy.get_score() for enemy in enemies_g if enemy.is_killed())
            draw_text(screen, str(score), 18, width // 2, 10)

            # Control game sprites appearance.
            # We shall place HERE before sprites gets update!
            manage_sprites_with_time(
                tt,
                (9,),
                (90,),
                elementary_enemy_list,
                [enemies_g, all_collided_objects_g]
            )
            manage_sprites_with_time(
                tt,
                (90,),
                (180,),
                mid_enemy_list,
                [enemies_g, all_collided_objects_g]
            )
            manage_sprites_with_time(
                tt,
                (180,),
                (225,),
                meteor_except_small_list,
                [enemies_g, all_collided_objects_g]
            )
            manage_sprites_with_time(
                tt,
                (225,),
                (300,),
                advanced_enemy_list,
                [enemies_g, all_collided_objects_g]
            )
            manage_sprites_with_time(
                tt,
                (21, 96, 210),
                (24, 99, 213),
                star_list,
                [stars_g, supplies_g, all_collided_objects_g]
            )
            manage_sprites_with_time(
                tt,
                (21, 129, 195),
                (24, 132, 198),
                bolt_list,
                [bolts_g, supplies_g, all_collided_objects_g]
            )
            manage_sprites_with_time(
                tt,
                (75, 246),
                (78, 258),
                pill_list,
                [pills_g, supplies_g, all_collided_objects_g]
            )
            manage_sprites_with_time(
                tt,
                (174, 237),
                (177, 240),
                shield_list,
                [shields_g, supplies_g, all_collided_objects_g]
            )
            manage_sprites_with_time(
                tt,
                (0,),
                (315,),
                meteor_small_list,
                [enemies_g, all_collided_objects_g]
            )

            # Draw explosions.
            explosions_g.update()
            explosions_g.draw(screen)

            # Draw player plane.
            players_g.update()
            players_g.draw(screen)

            # Draw enemies.
            enemies_g.update()
            enemies_g.draw(screen)

            # Draw lasers.
            lasers_g.update()
            lasers_g.draw(screen)

            # Draw shield.
            protection_g.update()
            protection_g.draw(screen)

            # Draw supplies.
            supplies_g.update()
            supplies_g.draw(screen)

            # Draw blood strip.
            temp = blood_strip_gap
            for i in range(player.get_blood()):
                pygame.draw.rect(
                    screen,
                    GREEN,
                    Rect((width - blood_strip_width - temp, 10), blood_strip_size),
                    0
                )
                temp = blood_strip_gap * (i + 2)

            # Draw player life.
            temp = player_life_gap
            for i in range(player.get_lives()):
                screen.blit(player_life, (width - player_life.get_rect().width - temp, 15 + blood_strip_height))
                temp = player_life_gap * (i + 5)

            # Flip.
            pygame.display.flip()

            # Determine how many lives left.
            if player.get_lives() < 0:
                run = False

        # Draw entry menu.
        # Retry?
        run = draw_exit(score)


if __name__ == '__main__':
    main()
