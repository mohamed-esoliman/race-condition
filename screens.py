import pygame
from constants import *
from assets import *

pygame.init()

font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)


def draw_menu_screen(window, menu_selection):
    window.fill((20, 18, 167))
    window.blit(background_image, (0, 0))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    window.blit(overlay, (0, 0))

    title_surface = font_large.render("RACE CONDITION", True, (255, 255, 255))
    window.blit(
        title_surface,
        title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4)),
    )

    subtitle = font_small.render("Select Difficulty", True, (200, 200, 200))
    window.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 50)))

    difficulties = ["EASY", "MEDIUM", "HARD"]
    difficulty_colors = [(80, 200, 80), (220, 200, 50), (220, 60, 60)]

    for i, (difficulty, difficulty_color) in enumerate(
        zip(difficulties, difficulty_colors)
    ):
        y = HEIGHT // 2 - 20 + i * 80
        is_selected = i == menu_selection
        box_rect = (WIDTH // 2 - 130, y - 20, 260, 58)

        if is_selected:
            pygame.draw.rect(window, difficulty_color, box_rect, border_radius=8)
            text_color = (0, 0, 0)
            description_color = (40, 40, 40)
        else:
            pygame.draw.rect(window, difficulty_color, box_rect, 2, border_radius=8)
            text_color = difficulty_color
            description_color = (160, 160, 160)

        difficulty_details = DIFFICULTIES[difficulty.lower()]
        label = font_small.render(difficulty, True, text_color)
        window.blit(label, label.get_rect(center=(WIDTH // 2, y - 2)))

        description = font_small.render(
            f"Time: {difficulty_details['timer']}s  HP: {difficulty_details['max_health']}  Chase: {difficulty_details['chase_range']}",
            True,
            description_color,
        )
        window.blit(description, description.get_rect(center=(WIDTH // 2, y + 22)))

    hint = font_small.render("UP/DOWN to select, ENTER to start", True, (160, 160, 160))
    window.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 40)))


def draw_overlay_screen(window, title, subtitle):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    window.blit(overlay, (0, 0))

    title_surface = font_large.render(title, True, (255, 255, 255))
    subtitle_surface = font_small.render(subtitle, True, (200, 200, 200))

    window.blit(
        title_surface,
        title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)),
    )
    window.blit(
        subtitle_surface,
        subtitle_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)),
    )


def draw_story_screen(window):
    window.fill((12, 12, 42))
    window.blit(background_image, (0, 0))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    window.blit(overlay, (0, 0))

    panel_rect = pygame.Rect(44, 36, WIDTH - 88, HEIGHT - 72)
    pygame.draw.rect(window, (22, 22, 38), panel_rect, border_radius=14)
    pygame.draw.rect(window, (90, 190, 255), panel_rect, 2, border_radius=14)

    title = font_medium.render("Mission Briefing", True, (255, 255, 255))
    window.blit(title, title.get_rect(center=(WIDTH // 2, panel_rect.top + 42)))

    text_rect = pygame.Rect(
        panel_rect.left + 28,
        panel_rect.top + 78,
        panel_rect.width - 56,
        panel_rect.height - 126,
    )
    text_y = text_rect.top
    line_height = font_small.get_linesize() + 3

    for line in STORY_LINES:
        if text_y + line_height > text_rect.bottom:
            break
        if line:
            line_surface = font_small.render(line, True, (225, 230, 245))
            window.blit(line_surface, (text_rect.left, text_y))
        text_y += line_height

    prompt_rect = pygame.Rect(
        panel_rect.left + 22, panel_rect.bottom - 46, panel_rect.width - 44, 24
    )
    pygame.draw.rect(window, (15, 25, 45), prompt_rect, border_radius=6)
    if (pygame.time.get_ticks() // 450) % 2 == 0:
        prompt = font_small.render(
            "Press ENTER or SPACE to begin", True, (150, 230, 255)
        )
        window.blit(prompt, prompt.get_rect(center=prompt_rect.center))
