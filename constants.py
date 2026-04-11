WIDTH = 720
HEIGHT = 512
WORLD_WIDTH = 4608

TILE_WIDTH = 48
TILE_HEIGHT = 32

PLAYER_WALKING_WIDTH = 72
PLAYER_WALKING_HEIGHT = 96
PLAYER_JUMPING_WIDTH = 84
PLAYER_JUMPING_HEIGHT = 108

PLAYER_X = WIDTH / 2
PLAYER_Y = HEIGHT * 0.8 - PLAYER_WALKING_HEIGHT

GRAVITY = 0.5
FRICTION = 0.4

PLAYER_VELOCITY_X = 5
PLAYER_VELOCITY_Y = -14

WALKING_ANIMATION_SPEED = 8

HEALTH_BAR_X = 16
HEALTH_BAR_Y = 16
HEALTH_BAR_W = 160
HEALTH_BAR_H = 14

ENEMY_WIDTH = 64
ENEMY_HEIGHT = 48
ENEMY_VELOCITY_X = 2
ENEMY_VELOCITY_Y = 2
ENEMY_CHASE_RANGE = 220

GATE_WIDTH = 48
GATE_HEIGHT = 64

POWERUP_SIZE = 24

Y_ground = HEIGHT - TILE_HEIGHT
Y_level2 = HEIGHT - TILE_HEIGHT * 3
Y_level3 = HEIGHT - TILE_HEIGHT * 5
Y_level4 = HEIGHT - TILE_HEIGHT * 7
Y_level5 = HEIGHT - TILE_HEIGHT * 9
Y_level6 = HEIGHT - TILE_HEIGHT * 11

# Game states
MENU = "menu"
STORY = "story"
PLAYING = "playing"
GAME_OVER = "game_over"
WIN = "win"

POWERUP_BONUS = 15
BG_MUSIC = "decisions_bg_music.mp3"
TICKING_LOOP = "ticking_sound_effect.mp3"
HURT_SFX = "hurt_sound_effect.mp3"
COLLECT_SFX = "collect_sound_effect.mp3"
JUMP_SFX = "jump_sound_effect.mp3"
BG_MUSIC_VOLUME = 0.85
TICKING_VOLUME = 0.1

LASER_HEIGHT = 48
LASER_ON_DURATION = 120
LASER_OFF_DURATION = 120
LASER_DAMAGE = 20

TIMER_START = 180

DIFFICULTIES = {
    "easy": {
        "timer": 90,
        "max_health": 100,
        "chase_range": 200,
    },
    "medium": {
        "timer": 45,
        "max_health": 50,
        "chase_range": 500,
    },
    "hard": {
        "timer": 20,
        "max_health": 30,
        "chase_range": 1000,
    },
}

STORY_LINES = [
    "The year is 2050. You are the last human in a facility controlled by an AI that",
    "has turned against humanity. Can you beat this 2D platformer game and",
    "escape before the facility locks down?",
    "",
    "The goal is simply to reach the exit before time runs out.",
    "Along the way, you will need to avoid robot enemies and navigate platforms.",
    "",
    "Be careful because any small mistake costs you time",
    "and you might fail to escape!",
]
