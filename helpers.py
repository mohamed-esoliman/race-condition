import pygame
import os


def load_image(name, scale=None):
    image = pygame.image.load(os.path.join("assets", name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image
