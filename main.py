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


def draw_world():
    for i in range(15):
        tiles.append(Tile(i * TILE_WIDTH, HEIGHT - TILE_HEIGHT, tile_image))

    for i in range(5):
        tiles.append(Tile((i + 6) * TILE_WIDTH, HEIGHT - TILE_HEIGHT * 3, tile_image))

    for i in range(4):
        tiles.append(Tile(i * TILE_WIDTH, HEIGHT - TILE_HEIGHT * 5, tile_image))

    for i in range(4):
        tiles.append(Tile((i + 11) * TILE_WIDTH, HEIGHT - TILE_HEIGHT * 5, tile_image))

    for i in range(3):
        tiles.append(Tile((i + 6) * TILE_WIDTH, HEIGHT - TILE_HEIGHT * 7, tile_image))

    enemies.append(Enemy(2 * TILE_WIDTH, HEIGHT - TILE_HEIGHT * 9))
    enemies.append(Enemy(10 * TILE_WIDTH, HEIGHT - TILE_HEIGHT * 9))


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
    elif player.x + player.width > WIDTH:
        player.x = WIDTH - player.width

    check_horizontal_collision(player)

    player.velocity_y += GRAVITY
    player.y += player.velocity_y

    check_vertical_collision(player)

    if player.damage_cooldown > 0:
        player.damage_cooldown -= 1

def move_enemies():
    for enemy in enemies:
        enemy.x += enemy.velocity_x
        if enemy.x < 0:
            enemy.x = 0
        elif enemy.x + enemy.width > WIDTH:
            enemy.x = WIDTH - enemy.width

        check_horizontal_collision(enemy)

        enemy.velocity_y += GRAVITY
        enemy.y += enemy.velocity_y

        check_vertical_collision(enemy)

        if player.colliderect(enemy) and player.damage_cooldown == 0:
            player.health = max(0, player.health - 10)
            player.damage_cooldown = 60

def move():
    move_player()
    move_enemies()

def draw():
    window.fill((20, 18, 167))

    window.blit(background_image, (0, 0))

    for tile in tiles:
        window.blit(tile.image, tile)

    player.update()
    window.blit(player.image, player)

    if player.damage_cooldown > 0 and (player.damage_cooldown // 6) % 2 == 0:
        flash = pygame.Surface((player.width, player.height), pygame.SRCALPHA)
        flash.fill((255, 0, 0, 120))
        window.blit(flash, player)

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

    for enemy in enemies:
        window.blit(enemy.image, enemy)


player = Player()
enemies = []
tiles = []
draw_world()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            exit()

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
    draw()

    pygame.display.update()
    clock.tick(60)
