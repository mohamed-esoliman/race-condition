import pygame

from constants import TILE_WIDTH, TILE_HEIGHT


class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_WIDTH, TILE_HEIGHT)
        self.image = image
