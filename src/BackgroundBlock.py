import pygame
from pygame.surface import Surface

class BackgroundBlock:
    SIZE = 120

    def __init__(self, top=0, left=0):
        self.sprite = pygame.image.load('src/res/BackgroundBlock.png')
        self.center = (top, left)

    def draw(self, surface: Surface):
        surface.blit(self.sprite, self.center)