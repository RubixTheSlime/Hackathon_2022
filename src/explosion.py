import pygame
from pygame.rect import Rect


class Explosion:
    def __init__(self, x, y):
        self.sprites = [pygame.image.load(f'src/res/Explode{i}.png').convert_alpha() for i in range(1, 7)]
        self.rect: Rect = self.sprites[0].get_rect()
        self.rect.centerx, self.rect.centery = x, y
        self.cull = False

    
