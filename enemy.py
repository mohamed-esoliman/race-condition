import pygame

from constants import (
    ENEMY_WIDTH,
    ENEMY_HEIGHT,
    ENEMY_VELOCITY_X,
    ENEMY_VELOCITY_Y,
    ENEMY_CHASE_RANGE,
)
from assets import enemy_left_image, enemy_right_image


class Enemy(pygame.Rect):
    def __init__(self, x, y, chase_range=ENEMY_CHASE_RANGE):
        pygame.Rect.__init__(self, x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.image = enemy_left_image
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "left"
        self.jumping = False
        self.movement_direction = 1
        self.chase_range = chase_range

    def update(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y

        if abs(dx) < self.chase_range and dy < 120:
            self.velocity_x = ENEMY_VELOCITY_X if dx > 0 else -ENEMY_VELOCITY_X
            self.velocity_y = ENEMY_VELOCITY_Y if dy > 0 else -ENEMY_VELOCITY_Y
        else:
            self.velocity_x = self.movement_direction * ENEMY_VELOCITY_X
            self.velocity_y = 0

        if self.velocity_x > 0:
            self.direction = "right"
            self.image = enemy_right_image
        else:
            self.direction = "left"
            self.image = enemy_left_image
