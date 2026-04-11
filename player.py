import pygame

from constants import (
    PLAYER_X,
    PLAYER_Y,
    PLAYER_WALKING_WIDTH,
    PLAYER_WALKING_HEIGHT,
    WALKING_ANIMATION_SPEED,
)
from assets import (
    player_walking_right_image,
    player_walking_left_image,
    player_walking_right_2_image,
    player_walking_left_2_image,
    player_jumping_right_image,
    player_jumping_left_image,
    player_walking_right_red_image,
    player_walking_left_red_image,
    player_walking_right_2_red_image,
    player_walking_left_2_red_image,
    player_jumping_right_red_image,
    player_jumping_left_red_image,
)

WALKING_FRAMES = {
    "right": [player_walking_right_image, player_walking_right_2_image],
    "left": [player_walking_left_image, player_walking_left_2_image],
}
WALKING_FRAMES_RED = {
    "right": [player_walking_right_red_image, player_walking_right_2_red_image],
    "left": [player_walking_left_red_image, player_walking_left_2_red_image],
}


class Player(pygame.Rect):
    def __init__(self, max_health=100):
        pygame.Rect.__init__(
            self, PLAYER_X, PLAYER_Y, PLAYER_WALKING_WIDTH, PLAYER_WALKING_HEIGHT
        )
        self.image = player_walking_right_image
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "right"
        self.jumping = False
        self.max_health = max_health
        self.health = max_health
        self.damage_cooldown = 0
        self.animation_timer = 0
        self.animation_frame = 0

    def update(self, damaged=False):
        if self.jumping:
        # if jumping, just set the image to the jumping image
            if self.direction == "right":
                self.image = (
                    player_jumping_right_red_image
                    if damaged
                    else player_jumping_right_image
                )
            elif self.direction == "left":
                self.image = (
                    player_jumping_left_red_image
                    if damaged
                    else player_jumping_left_image
                )
            self.animation_timer = 0
            self.animation_frame = 0
        elif self.velocity_x != 0:
        # if walking, update the animation according to the walking frames
            self.animation_timer += 1
            if self.animation_timer >= WALKING_ANIMATION_SPEED:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 2
            # normal image or red image
            frames = (
                WALKING_FRAMES_RED[self.direction]
                if damaged
                else WALKING_FRAMES[self.direction]
            )
            self.image = frames[self.animation_frame]
        else:
            self.animation_timer = 0
            self.animation_frame = 0
            frames = (
                WALKING_FRAMES_RED[self.direction]
                if damaged
                else WALKING_FRAMES[self.direction]
            )
            self.image = frames[0]
