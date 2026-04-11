import pygame
from sys import exit

from constants import *
from assets import *
from player import Player
from soundManager import SoundManager
from screens import draw_overlay_screen, draw_menu_screen, draw_story_screen

from levels.level1 import level1
from levels.level2 import level2
from levels.level3 import level3

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Race Condition")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)

LEVELS = [level1, level2, level3]
current_level_index = 0

current_difficulty = DIFFICULTIES["medium"]
menu_selection = 1  # 1 is medium

sound_manager = SoundManager.getInstance()
background_audio_started = False
ticking_sound_channel = None


def start_background_audio():
    global background_audio_started, ticking_sound_channel
    if background_audio_started:
        return
    sound_manager.playBGM(BG_MUSIC)
    pygame.mixer.music.set_volume(BG_MUSIC_VOLUME)
    ticking_sound_channel = sound_manager.playSFX(TICKING_LOOP, loops=-1)
    if ticking_sound_channel is not None:
        ticking_sound_channel.set_volume(TICKING_VOLUME)
    background_audio_started = True


def load_level(level_index):
    level = LEVELS[level_index]
    tiles = level.build_tiles()
    enemies = level.build_enemies(chase_range=current_difficulty["chase_range"])
    powerups = level.build_powerups()
    lasers = level.build_lasers()
    gate = level.build_gate()
    return tiles, enemies, powerups, lasers, gate


def reset_game(level_index=0):
    player = Player(max_health=current_difficulty["max_health"])
    tiles, enemies, powerups, lasers, gate = load_level(level_index)
    time_remaining = float(current_difficulty["timer"])
    game_state = PLAYING
    return player, tiles, enemies, powerups, lasers, gate, time_remaining, game_state


game_state = MENU
player = None
tiles = None
enemies = None
powerups = None
lasers = None
gate = None
time_remaining = None

# Collision detection

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


# Movement for player

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


# Movement for enemies

def move_enemies():
    for enemy in enemies:
        enemy.update(player.x, player.y)

        prev_vx = enemy.velocity_x
        enemy.x += enemy.velocity_x

        if enemy.x <= 0:
            enemy.x = 0
            enemy.movement_direction = 1
        elif enemy.x + enemy.width >= WORLD_WIDTH:
            enemy.x = WORLD_WIDTH - enemy.width
            enemy.movement_direction = -1

        check_horizontal_collision(enemy)

        if prev_vx != 0 and enemy.velocity_x == 0:
            enemy.movement_direction *= -1

        enemy.velocity_y += GRAVITY
        enemy.y += enemy.velocity_y

        check_vertical_collision(enemy)

        if (
            get_player_damage_rect(player).colliderect(get_enemy_damage_rect(enemy))
            and player.damage_cooldown == 0
        ):
            # player takes damage
            player.health = max(0, player.health - 10)
            player.damage_cooldown = 60
            sound_manager.playSFX(HURT_SFX)


# Update lasers

def update_lasers():
    for laser in lasers:
        laser.update()
        if laser.on and player.damage_cooldown == 0:
            # player takes damage
            if get_player_damage_rect(player).colliderect(laser):
                player.health = max(0, player.health - LASER_DAMAGE)
                player.damage_cooldown = 60
                sound_manager.playSFX(HURT_SFX)


# Main game loop

def move():
    move_player()
    move_enemies()
    update_lasers()


def get_player_damage_rect(player_rect):
    # I made this rect smaller to make it easier to avoid enemies
    damage_rect = player_rect.inflate(-22, -24)
    damage_rect.midbottom = player_rect.midbottom
    return damage_rect


def get_enemy_damage_rect(enemy_rect):
    # I made this rect smaller to make it easier to avoid enemies
    damage_rect = enemy_rect.inflate(-16, -10)
    damage_rect.midbottom = enemy_rect.midbottom
    return damage_rect


def draw():
    camera_x = max(0, min(player.x - WIDTH // 2, WORLD_WIDTH - WIDTH))

    window.fill((20, 18, 167))
    window.blit(background_image, (0, 0))

    for tile in tiles:
        window.blit(tile.image, (tile.x - camera_x, tile.y))

    for laser in lasers:
        window.blit(laser.image, (laser.x - camera_x, laser.y))

    window.blit(gate_image, (gate.x - camera_x, gate.y))

    for powerup in powerups:
        if not powerup.collected:
            powerup_x = int(powerup.x + 12 - camera_x)
            powerup_y = int(powerup.y + 12)
            pygame.draw.circle(window, (0, 200, 160), (powerup_x, powerup_y), 12)
            pygame.draw.circle(window, (180, 255, 235), (powerup_x, powerup_y), 6)

    # logic for flashing red when player is damaged
    is_flashing_red = (
        player.damage_cooldown > 0 and (player.damage_cooldown // 6) % 2 == 0
    )
    player.update(damaged=is_flashing_red)
    player_x = player.x - camera_x
    window.blit(player.image, (player_x, player.y))

    for enemy in enemies:
        window.blit(enemy.image, (enemy.x - camera_x, enemy.y))

    # logic for the health bar
    pygame.draw.rect(window, (60, 0, 0), (HEALTH_BAR_X, HEALTH_BAR_Y, HEALTH_BAR_W, HEALTH_BAR_H), border_radius=4)
    pygame.draw.rect(
        window,
        (220, 40, 40),
        (HEALTH_BAR_X, HEALTH_BAR_Y, int(HEALTH_BAR_W * player.health / player.max_health), HEALTH_BAR_H),
        border_radius=4,
    )
    pygame.draw.rect(
        window, (255, 255, 255), (HEALTH_BAR_X, HEALTH_BAR_Y, HEALTH_BAR_W, HEALTH_BAR_H), 1, border_radius=4
    )

    # timer
    seconds = max(0, int(time_remaining))
    timer_string = f"{seconds // 60}:{seconds % 60:02d}"
    if time_remaining > 30:
        timer_color = (255, 255, 255)
    elif time_remaining > 15:
        timer_color = (255, 220, 50)
    else:
        timer_color = (255, 60, 60)

    timer_surface = font_small.render(timer_string, True, timer_color)
    window.blit(timer_surface, timer_surface.get_rect(center=(WIDTH // 2, 24)))

    # level number
    level_surface = font_small.render(
        f"Level {current_level_index + 1}/{len(LEVELS)}", True, (255, 255, 255)
    )
    window.blit(level_surface, (16, 40))

    # game over and win screens
    if game_state == GAME_OVER:
        draw_overlay_screen(window, "GAME OVER", "R: restart level  Q: back to menu")
    elif game_state == WIN:
        draw_overlay_screen(window, "YOU FINISHED ALL LEVELS!", "R: play again  Q: back to menu")


delta_time = 0.0

while True:
    start_background_audio()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_UP:
                    menu_selection = (menu_selection - 1) % 3
                elif event.key == pygame.K_DOWN:
                    menu_selection = (menu_selection + 1) % 3
                elif event.key == pygame.K_RETURN:
                    difficulty_keys = ["easy", "medium", "hard"]
                    current_difficulty = DIFFICULTIES[difficulty_keys[menu_selection]]
                    game_state = STORY
            elif game_state == STORY:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    current_level_index = 0
                    (
                        player,
                        tiles,
                        enemies,
                        powerups,
                        lasers,
                        gate,
                        time_remaining,
                        game_state,
                    ) = reset_game(current_level_index)
            else:
                if event.key == pygame.K_r:
                    if game_state == WIN:
                        current_level_index = 0
                    (
                        player,
                        tiles,
                        enemies,
                        powerups,
                        lasers,
                        gate,
                        time_remaining,
                        game_state,
                    ) = reset_game(current_level_index)
                elif event.key == pygame.K_q:
                    game_state = MENU

    if game_state == MENU:
        draw_menu_screen(window, menu_selection)
    elif game_state == STORY:
        draw_story_screen(window)
    elif game_state == PLAYING:
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
            sound_manager.playSFX(JUMP_SFX)

        move()

        time_remaining -= delta_time

        for powerup in powerups:
            if not powerup.collected and player.colliderect(powerup):
                powerup.collected = True
                time_remaining += POWERUP_BONUS
                sound_manager.playSFX(COLLECT_SFX)

        if time_remaining <= 0 or player.health <= 0:
            game_state = GAME_OVER

        if player.colliderect(gate):
            if current_level_index < len(LEVELS) - 1:
                current_level_index += 1
                (
                    player,
                    tiles,
                    enemies,
                    powerups,
                    lasers,
                    gate,
                    time_remaining,
                    game_state,
                ) = reset_game(current_level_index)
            else:
                game_state = WIN

        draw()
    else:
        draw()

    pygame.display.update()
    delta_time = clock.tick(60) / 1000.0
