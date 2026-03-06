from constants import *
from helpers import load_image


background_image = load_image("background.png")
background_image = load_image("background.png", (WIDTH, HEIGHT))
icon = load_image("icon.png", (32, 32))

player_walking_right_image = load_image(
    "player_walking_right.png", (PLAYER_WALKING_WIDTH, PLAYER_WALKING_HEIGHT)
)
player_walking_left_image = load_image(
    "player_walking_left.png", (PLAYER_WALKING_WIDTH, PLAYER_WALKING_HEIGHT)
)
player_jumping_right_image = load_image(
    "player_jumping_right.png", (PLAYER_JUMPING_WIDTH, PLAYER_JUMPING_HEIGHT)
)
player_jumping_left_image = load_image(
    "player_jumping_left.png", (PLAYER_JUMPING_WIDTH, PLAYER_JUMPING_HEIGHT)
)
enemy_left_image = load_image("enemy_left.png", (ENEMY_WIDTH, ENEMY_HEIGHT))
enemy_right_image = load_image("enemy_right.png", (ENEMY_WIDTH, ENEMY_HEIGHT))
tile_image = load_image("floor_tile.png", (TILE_WIDTH, TILE_HEIGHT))
