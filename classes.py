import random

import numpy as np

import pygame
from pygame.locals import *

SCREENRECT = pygame.Rect(0, 0, 1280, 720)
TRANSPARENT = (0, 0, 0, 0)

# This global constant serves as a very useful convenience for me.
DIRECT_SHOOT_DICT = {K_LEFT: (-1, 0),
                     K_RIGHT: (1, 0),
                     K_UP: (0, -1),
                     K_DOWN: (0, 1)}

DIRECT_DICT = {K_a: (-1, 0),
               K_d: (1, 0),
               K_w: (0, -1),
               K_s: (0, 1)}


class Player(pygame.sprite.Sprite):
    """
    This class will represent our user controlled character.
    """
    SIZE = (50, 50)
    shot_speed = 10
    shot_delay = 100
    last_shot_time = 0
    speed = 3
    damage = 10
    range = 2000
    direction = (0, 0)

    def __init__(self, pos):
        """
        The pos argument is a tuple for the center of the player (x,y);
        speed is given in pixels/frame.
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = pygame.Rect((0, 0), Player.SIZE)
        self.rect.center = pos
        self.image = self.make_image()

    def make_image(self):
        """
        Creates our hero (a red circle with a black outline).
        """
        image = pygame.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pygame.draw.rect(image, pygame.Color("black"), image_rect)
        pygame.draw.rect(image, pygame.Color("blue"), image_rect.inflate(-12, -12))
        return image

    def update(self):
        """
        Updates our player appropriately every frame.
        """
        # for key in DIRECT_DICT:
        #     if keys[key]:
        #         self.rect.move_ip(DIRECT_DICT[key][0] * self.speed, DIRECT_DICT[key][1] * self.speed)
        self.rect.move_ip(self.direction[0] * self.speed, self.direction[1] * self.speed)
        self.rect.clamp_ip(SCREENRECT)  # Keep player on screen.

    def getpos(self):
        # returns the position from which the shot will be fired from
        return self.rect.center

    def getDamage(self):
        return self.damage


class Shot(pygame.sprite.Sprite):
    def __init__(self, startpos, direction, speed, size=10, range=100):
        """
        The pos argument is a tuple for the center of the player (x,y);
        speed is given in pixels/frame.
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.speed = speed
        self.direction = direction
        self.range = range
        self.startpos = startpos

        self.rect = pygame.Rect((0, 0), (size, size))
        self.rect.center = startpos
        self.image = self.make_image()

    def make_image(self):
        """
        Creates our hero (a red circle with a black outline).
        """
        image = pygame.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pygame.draw.rect(image, pygame.Color("blue"), image_rect)
        return image

    def update(self):
        self.rect.move_ip(self.direction[0] * self.speed, self.direction[1] * self.speed)
        if max(self.rect) > max(SCREENRECT) or min(self.rect) < 0:
            self.kill()
        if np.linalg.norm(self.startpos - np.array(self.rect.center)) > self.range:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    last_shot_time = 0

    def __init__(self, pos, type=0, size=50, speed=2, shot_speed=2, shot_delay=2000, health=3, direction=(0, 0),
                 growthRate=1):
        """
        The pos argument is a tuple for the center of the player (x,y);
        speed is given in pixels/frame.
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.type = type
        self.size = size
        self.speed = speed
        self.shot_speed = shot_speed
        self.shot_delay = shot_delay
        self.direction = direction
        self.health = health
        self.growthRate = growthRate

        self.rect = pygame.Rect((0, 0), (size, size))
        try:
            self.rect.center = pos
        except:
            self.rect.center = (0, 0)
        self.image = self.make_image()

    def make_image(self):
        """
        Creates our hero (a red circle with a black outline).
        """
        image = pygame.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pygame.draw.rect(image, pygame.Color("black"), image_rect)
        if self.type == 0:
            pygame.draw.rect(image, pygame.Color("red"), image_rect.inflate(-12, -12))
        elif self.type == 1:
            pygame.draw.rect(image, pygame.Color("yellow"), image_rect.inflate(-12, -12))
        elif self.type == 2:
            pygame.draw.rect(image, pygame.Color("brown"), image_rect.inflate(-12, -12))
        return image

    def update(self):
        self.rect.move_ip(self.direction[0] * self.speed, self.direction[1] * self.speed)
        if max(self.rect) > max(SCREENRECT) or min(self.rect) < 0:
            self.kill()

    def chase(self, playerpos):
        temp = np.array([playerpos[0] - self.getpos()[0], playerpos[1] - self.getpos()[1]])
        norm = np.sqrt((temp ** 2).sum())
        if norm != 0:
            self.direction = temp / norm

    def getpos(self):
        return self.rect.center

    def gettype(self):
        return self.type

    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def shoot(self, playerpos):
        Enemy(np.array(self.getpos()),
              speed=self.shot_speed,
              size=25,
              health=1,
              type=0)


class Powerup(pygame.sprite.Sprite):
    # TODO actually implement this
    def __init__(self, pos, type=0, size=30):
        """
        The pos argument is a tuple for the center of the player (x,y);
        speed is given in pixels/frame.
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.type = type
        self.size = size

        self.rect = pygame.Rect((0, 0), (size, size))
        try:
            self.rect.center = pos
        except:
            self.rect.center = (0, 0)
        self.image = self.make_image()

    def make_image(self):
        """
        Creates our hero (a red circle with a black outline).
        """
        image = pygame.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pygame.draw.rect(image, pygame.Color("black"), image_rect)
        pygame.draw.rect(image, pygame.Color("green"), image_rect.inflate(-12, -12))
        return image
