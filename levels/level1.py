from constants import *
from assets import tile_image as floor_tile_image
from .level_generator import LevelGenerator

platform_positions = [
    (6, 3, Y_level2),
    (12, 3, Y_level3),
    (19, 4, Y_level2),
    (26, 3, Y_level3),
    (36, 3, Y_level2),
    (41, 4, Y_level3),
    (49, 3, Y_level2),
    (57, 3, Y_level4),
    (64, 3, Y_level3),
    # (70, 4, Y_level2),
    (78, 3, Y_level3),
    (84, 2, Y_level4),
    (88, 2, Y_level5),
    (91, 2, Y_level6),
]

powerup_positions = [
    (13 * TILE_WIDTH + 12, Y_level3 - POWERUP_SIZE),
    (58 * TILE_WIDTH + 12, Y_level4 - POWERUP_SIZE),
    (89 * TILE_WIDTH + 12, Y_level5 - POWERUP_SIZE),
]

enemy_positions = [
    (22 * TILE_WIDTH, Y_ground - ENEMY_HEIGHT),
    (43 * TILE_WIDTH, Y_level3 - ENEMY_HEIGHT),
    (72 * TILE_WIDTH, Y_ground - ENEMY_HEIGHT),
]

laser_positions = [
    (30 * TILE_WIDTH, Y_ground - LASER_HEIGHT, 4),
    (70 * TILE_WIDTH, Y_ground - LASER_HEIGHT, 4),
]   

gate_position = (92 * TILE_WIDTH, Y_ground - GATE_HEIGHT)


level1 = LevelGenerator(
    tile_image=floor_tile_image,
    platform_positions=platform_positions,
    powerup_positions=powerup_positions,
    enemy_positions=enemy_positions,
    laser_positions=laser_positions,
    gate_position=gate_position,
)