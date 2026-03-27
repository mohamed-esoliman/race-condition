import pygame
from sys import exit

from constants import *
from assets import *
from player import Player
from tile import Tile
from enemy import Enemy

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Race Condition")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
font_large = pygame.font.SysFont(None, 72)
font_small = pygame.font.SysFont(None, 36)
font_tiny = pygame.font.SysFont(None, 24)

PLAYING = "playing"
GAME_OVER = "game_over"
WIN = "win"

POWERUP_SIZE = 24
POWERUP_BONUS = 15


class PowerUp(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, POWERUP_SIZE, POWERUP_SIZE)
        self.collected = False


Y_ground = HEIGHT - TILE_HEIGHT 
Y_level2 = HEIGHT - TILE_HEIGHT * 3 
Y_level3 = HEIGHT - TILE_HEIGHT * 5 
Y_level4 = HEIGHT - TILE_HEIGHT * 7 
Y_level5 = HEIGHT - TILE_HEIGHT * 9 
Y_level6 = HEIGHT - TILE_HEIGHT * 11 


def build_tiles():
    tiles = []

    # Ground
    for i in range(96):
        tiles.append(Tile(i * TILE_WIDTH, Y_ground, tile_image))

    platforms = [
        # Section 1
        (2, 4, Y_level2),
        (7, 3, Y_level3),
        (11, 3, Y_level4),
        (15, 4, Y_level3),
        (20, 3, Y_level2),

        # Section 2
        (25, 3, Y_level2),
        (29, 2, Y_level3),
        (32, 2, Y_level4),
        (35, 3, Y_level5),
        (39, 2, Y_level4),
        (42, 2, Y_level3),
        (45, 3, Y_level2),
        
        # Section 3
        (49, 3, Y_level3),
        (53, 2, Y_level4),
        (56, 2, Y_level5),
        (59, 2, Y_level6),
        (62, 2, Y_level5),
        (65, 2, Y_level4),
        (68, 3, Y_level3),
        
        # Section 4
        (73, 3, Y_level2),
        (77, 2, Y_level3),
        (80, 2, Y_level4),
        (83, 2, Y_level5),
        (86, 2, Y_level6),
        (89, 2, Y_level5),
        (91, 2, Y_level6),  # gate
        (93, 2, Y_level5),
    ]

    for start, length, y in platforms:
        for i in range(length):
            tiles.append(Tile((start + i) * TILE_WIDTH, y, tile_image))

    return tiles


def build_powerups():

    powerup_positions = [
        (4 * TILE_WIDTH + 12, Y_level2 - POWERUP_SIZE),
        (12 * TILE_WIDTH + 12, Y_level4 - POWERUP_SIZE),
        (21 * TILE_WIDTH + 12, Y_level2 - POWERUP_SIZE),
        (30 * TILE_WIDTH + 12, Y_level3 - POWERUP_SIZE),
        (36 * TILE_WIDTH + 12, Y_level5 - POWERUP_SIZE),
        (43 * TILE_WIDTH + 12, Y_level3 - POWERUP_SIZE),
    ]
    return [PowerUp(x, y) for x, y in powerup_positions]


def build_enemies():
    enemy_positions = [
        (8 * TILE_WIDTH, Y_level3 - ENEMY_HEIGHT),
        (16 * TILE_WIDTH, Y_level3 - ENEMY_HEIGHT),
        (35 * TILE_WIDTH, Y_level5 - ENEMY_HEIGHT),
        (45 * TILE_WIDTH, Y_level2 - ENEMY_HEIGHT),
        (56 * TILE_WIDTH, Y_level5 - ENEMY_HEIGHT),
    ]
    return [Enemy(x, y) for x, y in enemy_positions]

gate = pygame.Rect(
    92 * TILE_WIDTH,
    Y_level6 - GATE_HEIGHT,
    GATE_WIDTH,
    GATE_HEIGHT,
)

tiles = build_tiles()


def reset_game():
    """
    Reset the game state
    Returns: player, enemies, powerups, time_remaining, game_state
    """
    player = Player()
    enemies = build_enemies()
    powerups = build_powerups()
    time_remaining = float(TIMER_START)
    game_state = PLAYING
    return player, enemies, powerups, time_remaining, game_state


player, enemies, powerups, time_remaining, game_state = reset_game()


# Collisions


def check_collision(collider):
    for tile in tiles:
        if collider.colliderect(tile):
            return tile
    return None


def check_horizontal_collision(collider):
    tile = check_collision(collider)
    if tile is not None:
        if collider.velocity_x < 0:
            collider.x = tile.x + tile.width
        elif collider.velocity_x > 0:
            collider.x = tile.x - collider.width
        collider.velocity_x = 0


def check_vertical_collision(collider):
    tile = check_collision(collider)
    if tile is not None:
        if collider.velocity_y < 0:
            collider.y = tile.y + tile.height
        elif collider.velocity_y > 0:
            collider.y = tile.y - collider.height
            collider.jumping = False
        collider.velocity_y = 0


# Movement


def move_player():
    if player.direction == "left" and player.velocity_x < 0:
        player.velocity_x += FRICTION
    elif player.direction == "right" and player.velocity_x > 0:
        player.velocity_x -= FRICTION
    else:
        player.velocity_x = 0

    player.x += player.velocity_x
    if player.x < 0:
        player.x = 0
    elif player.x + player.width > WORLD_WIDTH:
        player.x = WORLD_WIDTH - player.width

    check_horizontal_collision(player)

    player.velocity_y += GRAVITY
    player.y += player.velocity_y

    check_vertical_collision(player)

    if player.damage_cooldown > 0:
        player.damage_cooldown -= 1


def move_enemies():
    for enemy in enemies:
        enemy.update_ai(player.x, player.y)

        prev_vx = enemy.velocity_x
        enemy.x += enemy.velocity_x

        if enemy.x <= 0:
            enemy.x = 0
            enemy.patrol_direction = 1
        elif enemy.x + enemy.width >= WORLD_WIDTH:
            enemy.x = WORLD_WIDTH - enemy.width
            enemy.patrol_direction = -1

        check_horizontal_collision(enemy)

        if prev_vx != 0 and enemy.velocity_x == 0:
            enemy.patrol_direction *= -1

        enemy.velocity_y += GRAVITY
        enemy.y += enemy.velocity_y

        check_vertical_collision(enemy)

        if (
            get_player_damage_rect(player).colliderect(get_enemy_damage_rect(enemy))
            and player.damage_cooldown == 0
        ):
            player.health = max(0, player.health - 10)
            player.damage_cooldown = 60


def move():
    move_player()
    move_enemies()


def get_player_damage_rect(player_rect):
    damage_rect = player_rect.inflate(-22, -24)
    damage_rect.midbottom = player_rect.midbottom
    return damage_rect


def get_enemy_damage_rect(enemy_rect):
    damage_rect = enemy_rect.inflate(-16, -10)
    damage_rect.midbottom = enemy_rect.midbottom
    return damage_rect


# Rendering


def draw_overlay(title, subtitle):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    window.blit(overlay, (0, 0))

    window.blit(
        font_large.render(title, True, (255, 255, 255)),
        font_large.render(title, True, (255, 255, 255)).get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 40)
        ),
    )
    window.blit(
        font_small.render(subtitle, True, (200, 200, 200)),
        font_small.render(subtitle, True, (200, 200, 200)).get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 20)
        ),
    )


def draw():
    camera_x = max(0, min(player.x - WIDTH // 2, WORLD_WIDTH - WIDTH))

    window.fill((20, 18, 167))
    window.blit(background_image, (0, 0))

    for tile in tiles:
        window.blit(tile.image, (tile.x - camera_x, tile.y))

    window.blit(gate_image, (gate.x - camera_x, gate.y))

    # Power-ups
    for powerup in powerups:
        if not powerup.collected:
            powerup_x = int(powerup.x + 12 - camera_x)
            powerup_y = int(powerup.y + 12)
            pygame.draw.circle(window, (0, 200, 160), (powerup_x, powerup_y), 12)
            pygame.draw.circle(window, (180, 255, 235), (powerup_x, powerup_y), 6)

    # Player
    is_flashing_red = (
        player.damage_cooldown > 0 and (player.damage_cooldown // 6) % 2 == 0
    )
    player.update(damaged=is_flashing_red)
    player_x = player.x - camera_x
    window.blit(player.image, (player_x, player.y))

    # Enemies
    for enemy in enemies:
        window.blit(enemy.image, (enemy.x - camera_x, enemy.y))

    # Health bar
    bar_x, bar_y, bar_w, bar_h = 16, 16, 160, 14
    pygame.draw.rect(window, (60, 0, 0), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
    pygame.draw.rect(
        window,
        (220, 40, 40),
        (bar_x, bar_y, int(bar_w * player.health / 100), bar_h),
        border_radius=4,
    )
    pygame.draw.rect(
        window, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 1, border_radius=4
    )

    # Timer
    secs = max(0, int(time_remaining))
    timer_string = f"{secs // 60}:{secs % 60:02d}"
    if time_remaining > 30:
        timer_color = (255, 255, 255)
    elif time_remaining > 15:
        timer_color = (255, 220, 50)
    else:
        timer_color = (255, 60, 60)
    timer_surface = font_small.render(timer_string, True, timer_color)
    window.blit(timer_surface, timer_surface.get_rect(center=(WIDTH // 2, 24)))

    # Overlay
    if game_state == GAME_OVER:
        draw_overlay("GAME OVER", "Press R to restart")
    elif game_state == WIN:
        draw_overlay("YOU ESCAPED!", "Press R to play again")


# Main loop

delta_time = 0.0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if game_state in (GAME_OVER, WIN):
                player, enemies, powerups, time_remaining, game_state = reset_game()

    if game_state == PLAYING:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.velocity_x = -PLAYER_VELOCITY_X
            player.direction = "left"

        if keys[pygame.K_RIGHT]:
            player.velocity_x = PLAYER_VELOCITY_X
            player.direction = "right"

        if keys[pygame.K_SPACE] and not player.jumping:
            player.velocity_y = PLAYER_VELOCITY_Y
            player.jumping = True

        move()

        time_remaining -= delta_time

        # Power-up collection
        for powerup in powerups:
            if not powerup.collected and player.colliderect(powerup):
                powerup.collected = True
                time_remaining += POWERUP_BONUS

        if time_remaining <= 0 or player.health <= 0:
            game_state = GAME_OVER

        if player.colliderect(gate):
            game_state = WIN

    draw()

    pygame.display.update()
    delta_time = clock.tick(60) / 1000.0
