from constants import *
from assets import tile_image as floor_tile_image
from .level_generator import LevelGenerator

platform_positions = [
    (4, 3, Y_level2),
    (9, 2, Y_level3),
    (13, 3, Y_level4),
    (19, 2, Y_level3),
    # (24, 3, Y_level2),
    # (28, 2, Y_level4),
    (35, 2, Y_level5),
    (40, 3, Y_level3),
    # (46, 2, Y_level4),
    (51, 3, Y_level2),
    (57, 2, Y_level3),
    # (62, 2, Y_level4),
    (67, 2, Y_level5),
    # (72, 3, Y_level3),
    (78, 2, Y_level3),
    (82, 2, Y_level5),
    # (86, 2, Y_level4),
    (89, 2, Y_level3),
    (92, 2, Y_level4),
    (94, 2, Y_level5),
]

powerup_positions = [
    (14 * TILE_WIDTH + 12, Y_level4 - POWERUP_SIZE),
    (36 * TILE_WIDTH + 12, Y_level5 - POWERUP_SIZE),
    (68 * TILE_WIDTH + 12, Y_level5 - POWERUP_SIZE),
    (95 * TILE_WIDTH + 12, Y_level5 - POWERUP_SIZE),
]

enemy_positions = [
    (12 * TILE_WIDTH, Y_level4 - ENEMY_HEIGHT),
    (33 * TILE_WIDTH, Y_ground - ENEMY_HEIGHT),
    (52 * TILE_WIDTH, Y_level2 - ENEMY_HEIGHT),
    (74 * TILE_WIDTH, Y_level3 - ENEMY_HEIGHT),
    (89 * TILE_WIDTH, Y_level3 - ENEMY_HEIGHT),
]

laser_positions = [
    (24 * TILE_WIDTH, Y_ground - LASER_HEIGHT, 4),
    (43 * TILE_WIDTH, Y_ground - LASER_HEIGHT, 5),
    (60 * TILE_WIDTH, Y_ground - LASER_HEIGHT, 4),
    (84 * TILE_WIDTH, Y_ground - LASER_HEIGHT, 5),
]

gate_position = (95 * TILE_WIDTH, Y_level5 - GATE_HEIGHT)

level2 = LevelGenerator(
    tile_image=floor_tile_image,
    platform_positions=platform_positions,
    powerup_positions=powerup_positions,
    enemy_positions=enemy_positions,
    laser_positions=laser_positions,
    gate_position=gate_position,
)
