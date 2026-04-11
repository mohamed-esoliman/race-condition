import pygame

from constants import LASER_HEIGHT, LASER_ON_DURATION, LASER_OFF_DURATION, TILE_WIDTH
from assets import laser_on_image, laser_off_image


class Laser(pygame.Rect):
    def __init__(
        self,
        x,
        y,
        width,
        on_duration=LASER_ON_DURATION,
        off_duration=LASER_OFF_DURATION,
    ):
        total_width = width * TILE_WIDTH
        pygame.Rect.__init__(self, x, y, total_width, LASER_HEIGHT)
        self.image_on = pygame.transform.scale(
            laser_on_image, (total_width, LASER_HEIGHT)
        )
        self.image_off = pygame.transform.scale(
            laser_off_image, (total_width, LASER_HEIGHT)
        )
        self.on = True
        self.on_duration = on_duration
        self.off_duration = off_duration
        self.timer = on_duration
        self.image = self.image_on

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.on = not self.on
            self.timer = self.on_duration if self.on else self.off_duration
            self.image = self.image_on if self.on else self.image_off
