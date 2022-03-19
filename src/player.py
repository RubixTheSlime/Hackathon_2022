import pygame
from pygame import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from inputstate import InputState


class Player:
    def __init__(self):
        self.grounded = False
        self.velocity = Vector2(0, 0)
        self.sprite = pygame.image.load('src/res/Erik.png')
        self.rect = self.sprite.get_rect(center=(100, 100))

    def handle_movement(self, inputState: InputState):
        if inputState.jump:
            if self.grounded:
                self.velocity.y = 100

        if inputState.left:
            if self.velocity.x > -400:
                self.velocity.x -= 10
        elif inputState.right:
            if self.velocity.x < 400:
                self.velocity.x += 10
        else:
            if abs(self.velocity.x) < 10:
                self.velocity.x = 0
            else:
                self.velocity.x *= 0.85

        if inputState.boost:
            pass

    def update(self, dt, blocks):
        self.velocity.y += (100 * dt)

        self.rect = self.rect.move((self.velocity.x*dt, 0))
        # detect x collision with blocks
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.x > 0:
                    self.rect.right = block.rect.left
                else: # self.velocity.x is negative
                    self.rect.left = block.rect.right
                self.velocity.x = 0

        self.rect = self.rect.move((0, self.velocity.y*dt))
        # detect y collision with blocks
        self.grounded = False
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = block.rect.top
                    self.grounded = True
                else: # self.velocity.y is negative
                    self.rect.top = block.rect.bottom
                self.velocity.y = 0

    def draw(self, surface: Surface):
        surface.blit(self.sprite, self.rect)
