import os
import random

import pygame
from pygame.surface import Surface


class BackgroundBlock:
    SIZE = 120

    def __init__(self, top: int = None, left: int = None, copy_from: 'BackgroundBlock' = None):
        if copy_from is not None:
            self.path = copy_from.path
            self.sprite = pygame.image.load(self.path).convert()
            self.topleft = copy_from.topleft[:]
            return
        path_start = 'src/res/BackgroundBlock'
        self.path = os.path.join(path_start, random.choice(os.listdir(path_start)))
        self.sprite = pygame.image.load(self.path).convert()
        self.topleft = (top * 120, left * 120)

    def draw(self, surface: Surface) -> None:
        surface.blit(self.sprite, self.topleft)
