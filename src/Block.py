import pygame
from pygame import Vector2
from pygame import Surface

class Block:
    SIZE = 120
    
    def __init__(self, left=0, top=0):
        self.sprite = pygame.image.load('src/res/Block.png').convert()
        self.rect = self.sprite.get_rect(left=left, top=top, width = Block.SIZE, height = Block.SIZE)

    def update(self):
        pass

    def draw(self, surface: Surface):
        surface.blit(self.sprite, self.rect)