import pygame
from pygame import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from inputstate import InputState


class Player:
    def __init__(self):
        self.velocity = Vector2(0, 0)
        self.sprite = pygame.image.load('src/res/Erik.png')
        self.rect = self.sprite.get_rect()

    def handle_movement(self, inputState: InputState):
        pass

    def update(self, dt):
        self.rect.move(*(self.velocity * dt))

    def draw(self, surface: Surface):
        surface.blit(self.sprite, self.rect)
