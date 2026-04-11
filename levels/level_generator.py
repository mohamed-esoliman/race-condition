import pygame

from constants import *
from tile import Tile
from enemy import Enemy
from laser import Laser
from powerup import PowerUp


class LevelGenerator:
    def __init__(
        self,
        tile_image,
        platform_positions,
        powerup_positions,
        enemy_positions,
        laser_positions,
        gate_position,
    ):
        self.tile_image = tile_image
        self.platform_positions = platform_positions
        self.powerup_positions = powerup_positions
        self.enemy_positions = enemy_positions
        self.laser_positions = laser_positions
        self.gate_position = gate_position

    def build_tiles(self):
        tiles = []

        for i in range(96):
            tiles.append(Tile(i * TILE_WIDTH, Y_ground, self.tile_image))

        for start, length, y in self.platform_positions:
            for i in range(length):
                tiles.append(Tile((start + i) * TILE_WIDTH, y, self.tile_image))

        return tiles

    def build_powerups(self):
        return [PowerUp(x, y) for x, y in self.powerup_positions]

    def build_enemies(self, chase_range=None):
        if chase_range is not None:
            return [Enemy(x, y, chase_range) for x, y in self.enemy_positions]
        return [Enemy(x, y) for x, y in self.enemy_positions]

    def build_lasers(self):
        return [
            Laser(x, y, width=width)
            for x, y, width in self.laser_positions
        ]

    def build_gate(self):
        return pygame.Rect(
            self.gate_position[0],
            self.gate_position[1],
            GATE_WIDTH,
            GATE_HEIGHT,
        )
