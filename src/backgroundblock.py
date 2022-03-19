import os
import random

import pygame
from pygame.surface import Surface


class BackgroundBlock:
    SIZE = 120

    def __init__(self, top: int = None, left: int = None, copy_from: 'BackgroundBlock' = None):
        if copy_from is not None:
            self.path = copy_from.path
            self.topleft = copy_from.topleft[:]
            self.flip_x, self.flip_y = copy_from.flip_x, copy_from.flip_y
            self.sprite = pygame.transform.flip(pygame.image.load(self.path).convert(), self.flip_x, self.flip_y)
            return
        path_start = 'src/res/BackgroundBlock'
        self.path = os.path.join(path_start, random.choice(os.listdir(path_start)))
        self.flip_x = random.randint(0, 1)
        self.flip_y = random.randint(0, 1)
        self.sprite = pygame.transform.flip(pygame.image.load(self.path).convert(), self.flip_x, self.flip_y)
        self.topleft = (top * 120, left * 120)

    def draw(self, surface: Surface) -> None:
        surface.blit(self.sprite, self.topleft)
