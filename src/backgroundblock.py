import os
import random

import pygame
from pygame.surface import Surface


class BackgroundBlock:
    SIZE = 120

    def __init__(self, top: int = 0, left: int = 0):
        path_start = 'src/res/BackgroundBlock'
        path = os.path.join(path_start, random.choice(os.listdir(path_start)))
        self.sprite = pygame.image.load(path).convert()
        self.topleft = (top * 120, left * 120)

    def draw(self, surface: Surface) -> None:
        surface.blit(self.sprite, self.topleft)
