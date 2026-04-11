import pygame
from constants import POWERUP_SIZE


class PowerUp(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, POWERUP_SIZE, POWERUP_SIZE)
        self.collected = False
