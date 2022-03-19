import pygame
from pygame.surface import Surface


class BackgroundBlock:
    SIZE = 120

    def __init__(self, top: int = 0, left: int = 0):
        self.sprite = pygame.image.load('src/res/BackgroundBlock.png').convert()
        self.topleft = (top * 120, left * 120)

    def draw(self, surface: Surface) -> None:
        surface.blit(self.sprite, self.topleft)
