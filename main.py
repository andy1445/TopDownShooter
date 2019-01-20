#! /usr/bin/env python

"""
This script implements a basic sprite that can move in all 8 directions.
-Written by Sean J. McKiernan 'Mekire'
"""
import os
import random
import sys
from classes import *

CAPTION = "Move me with the Arrow Keys"
SCREENRECT = pygame.Rect(0, 0, 1280, 720)
TRANSPARENT = (0, 0, 0, 0)


def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption(CAPTION)
    winstyle = 1
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    background = pygame.Surface(SCREENRECT.size)
    background.fill(Color("white"))
    screen.blit(background, (0, 0))
    pygame.display.flip()
    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()
    fps = 60

    shots = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()

    Player.containers = all
    Shot.containers = shots, all
    Enemy.containers = enemies, all

    done = False
    maxShots = 100
    enemySpawnRate = .01
    powerupSpawnRate = .01

    player = Player(screen_rect.center)
    while not done:
        if not player.alive():
            return
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        tick = pygame.time.get_ticks()

        movedir = np.zeros(2)
        for key in DIRECT_DICT:
            if keys[key]:
                movedir += DIRECT_DICT[key]
        player.direction = movedir

        shootdir = np.zeros(2)
        shootBool = False
        for key in DIRECT_SHOOT_DICT:
            if keys[key]:
                shootdir += DIRECT_SHOOT_DICT[key]
                shootBool = True

        # shootdir += movedir #comment for isaac shooting styleasa
        if shootBool == True and tick > player.last_shot_time + player.shot_delay and len(
                shots) < maxShots:  # in milliseconds
            Shot(player.getpos(), shootdir, player.shot_speed, range=player.range)
            player.last_shot_time = tick

        # check to spawn enemy
        if random.random() < enemySpawnRate:
            enemySpawnRate += .0003
            type = random.choice((0, 1, 2))
            # type = 1
            if type == 0:  # chasers
                Enemy(np.array(player.getpos()) + np.random.choice((-150, 150, -200, 200), size=(2)),
                      speed=random.choice((2, 3)),
                      size=random.choice((20, 30, 40)),
                      health=random.choice((1, 2, 3)),
                      type=0)
            elif type == 1:  # growers
                Enemy(np.array(player.getpos()) + np.random.choice((-150, 150, -200, 200), size=(2)),
                      speed=random.choice((2, 3)),
                      size=random.choice((45, 55, 65)),
                      health=random.choice((3, 4, 5)),
                      growthRate=1.03,
                      type=1)
            elif type == 2:  # spawners
                Enemy(np.array(player.getpos()) + np.random.choice((-150, 150, -200, 200), size=(2)),
                      size=50,
                      health=random.choice((1, 2)),
                      type=2)

        for e in enemies:
            if e.gettype() == 0:
                # chase the player
                e.chase(player.getpos())
            elif e.gettype() == 1:
                pass
                # if random.random() < .6:
                #     e.kill()
                #     Enemy(e.getpos(),
                #           size=e.size * e.growthRate,
                #           health=e.health,
                #           growthRate=e.growthRate,
                #           type=1)
                # else:
                #     e.kill()
                #     Enemy(e.getpos(),
                #           size=e.size * e.growthRate,
                #           health=e.health,
                #           growthRate=1,
                #           type=0,
                #           speed=0)
            elif e.gettype() == 2:
                # spawn
                if tick > e.last_shot_time + e.shot_delay:
                    e.shoot(player.getpos())
                    e.last_shot_time = tick
        # spawn powerups
        # if random.random() < powerupSpawnRate:
        #     Powerup(random.choice(0,1,2,3))

        # Detect collisions
        for enemy in pygame.sprite.spritecollide(player, enemies, 1):
            player.kill()

        for enemy in pygame.sprite.groupcollide(enemies, shots, 0, 1).keys():
            enemy.damage(player.getDamage())

        all.clear(screen, background)
        all.update()
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        clock.tick(fps)

    sys.exit()


if __name__ == "__main__":
    main()
