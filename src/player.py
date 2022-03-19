import pygame
from pygame import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from inputstate import InputState


class Player:
    def __init__(self):
        self.grounded_frames_remaining = 0
        self.jump_timer = 0
        self.velocity = Vector2(0, 0)
        self.sprite = pygame.image.load('src/res/Erik.png')
        self.rect = self.sprite.get_rect(center=(100, 100))

    def handle_movement(self, inputState: InputState):
        if inputState.jump:
            if self.grounded_frames_remaining:
                self.jump_timer += 2

        target_speed = 400 * (inputState.right - inputState.left)
        if abs(self.velocity.x - target_speed) < 10:
            self.velocity.x = target_speed
        else:
            self.velocity.x += (target_speed - self.velocity.x) * 0.13

        if inputState.boost:
            pass

    def update(self, dt, blocks):
        if self.jump_timer:
            self.velocity.y = -600
            self.jump_timer -= 1
        else:
            target_speed = 1500
            if abs(self.velocity.y - target_speed) < 10:
                self.velocity.y = target_speed
            else:
                self.velocity.y += (target_speed - self.velocity.y) * 0.05

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
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.y >= 0:
                    self.rect.bottom = block.rect.top
                    self.grounded_frames_remaining = 10
                else: # self.velocity.y is negative
                    self.rect.top = block.rect.bottom
                self.velocity.y = 0

        if self.grounded_frames_remaining > 0:
            self.grounded_frames_remaining -= 1

    def draw(self, surface: Surface):
        surface.blit(self.sprite, self.rect)
