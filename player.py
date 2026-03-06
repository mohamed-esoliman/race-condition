import pygame

from constants import PLAYER_X, PLAYER_Y, PLAYER_WALKING_WIDTH, PLAYER_WALKING_HEIGHT
from assets import (
    player_walking_right_image,
    player_walking_left_image,
    player_jumping_right_image,
    player_jumping_left_image,
)


class Player(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(
            self, PLAYER_X, PLAYER_Y, PLAYER_WALKING_WIDTH, PLAYER_WALKING_HEIGHT
        )
        self.image = player_walking_right_image
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "right"
        self.jumping = False
        self.health = 100
        self.damage_cooldown = 0

    def update(self):
        if self.jumping:

            if self.direction == "right":
                self.image = player_jumping_right_image
            elif self.direction == "left":
                self.image = player_jumping_left_image
        else:

            if self.direction == "right":
                self.image = player_walking_right_image
            elif self.direction == "left":
                self.image = player_walking_left_image
