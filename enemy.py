import pygame

from constants import ENEMY_WIDTH, ENEMY_HEIGHT
from assets import enemy_left_image


class Enemy(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.image = enemy_left_image
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "left"
        self.jumping = False
