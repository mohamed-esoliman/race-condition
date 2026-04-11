from constants import *
from assets import tile_image as floor_tile_image
from .level_generator import LevelGenerator


platform_positions = [
    (4, 2, Y_level2),
    (8, 2, Y_level3),
    (12, 2, Y_level4),
    # (16, 2, Y_level5),
    (20, 2, Y_level6),
    (25, 2, Y_level5),
    (29, 2, Y_level4),
    (34, 2, Y_level3),
    (39, 2, Y_level2),
    (44, 2, Y_level4),
    # (48, 2, Y_level5),
    (52, 2, Y_level6),
    (57, 2, Y_level5),
    (61, 2, Y_level4),
    (66, 2, Y_level3),
    (71, 2, Y_level2),
    (75, 2, Y_level4),
    (79, 2, Y_level5),
    # (83, 2, Y_level6),
    (87, 2, Y_level5),
    (90, 2, Y_level6),
    (93, 2, Y_level5),
    (95, 1, Y_level6),
]

powerup_positions = [
    (21 * TILE_WIDTH + 12, Y_level6 - POWERUP_SIZE),
    (53 * TILE_WIDTH + 12, Y_level6 - POWERUP_SIZE),
    (91 * TILE_WIDTH + 12, Y_level6 - POWERUP_SIZE),
]

enemy_positions = [
    (10 * TILE_WIDTH, Y_level3 - ENEMY_HEIGHT),
    (27 * TILE_WIDTH, Y_level5 - ENEMY_HEIGHT),
    (45 * TILE_WIDTH, Y_level4 - ENEMY_HEIGHT),
    (58 * TILE_WIDTH, Y_level5 - ENEMY_HEIGHT),
    (76 * TILE_WIDTH, Y_level4 - ENEMY_HEIGHT),
    (88 * TILE_WIDTH, Y_level5 - ENEMY_HEIGHT),
]

laser_positions = [
    (14 * TILE_WIDTH, Y_ground - LASER_HEIGHT, 5),
    (30 * TILE_WIDTH, Y_ground - LASER_HEIGHT, 5),
    (47 * TILE_WIDTH, Y_ground - LASER_HEIGHT, 4),
    (64 * TILE_WIDTH, Y_ground - LASER_HEIGHT, 5),
    (81 * TILE_WIDTH, Y_ground - LASER_HEIGHT, 5),
]

gate_position = (95 * TILE_WIDTH, Y_level6 - GATE_HEIGHT)

level3 = LevelGenerator(
    tile_image=floor_tile_image,
    platform_positions=platform_positions,
    powerup_positions=powerup_positions,
    enemy_positions=enemy_positions,
    laser_positions=laser_positions,
    gate_position=gate_position,
)
