import pygame
from pygame import Vector2
from pygame import Surface

class Block:
    def __init__(self):
        self.sprite = pygame.image.load('src/res/Block.png')
        self.rect = self.surface.get_rect()

    def update(self):
        pass

    def draw(self, surface: Surface):
        surface.blit(self.sprite, self.rect)