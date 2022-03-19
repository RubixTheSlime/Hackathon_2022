import pygame
from pygame import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from inputstate import InputState


class Player:
    def __init__(self):
        self.grounded_time_remaining = 0
        self.jump_timer = 0
        self.explosion_timer = -1
        self.animation_timer = 0

        self.velocity = Vector2(0, 0)

        self.explosion_sprites = [ pygame.image.load(f'src/res/Explode{i}.png') for i in range(1, 7) ]
        self.explosion_rect = None

        self.sprites_right = [ pygame.image.load(f'src/res/Erik{x}.png') for x in ['', 'Left', '', 'Right'] ]
        self.sprites_left = [ pygame.transform.flip(surface, True, False) for surface in self.sprites_right ]
        self.facing_right = True

        self.rect = self.sprites_right[0].get_rect(center=(100, 100))
        # self.rect.height *= 0.95

    def handle_movement(self, inputState: InputState, dt):
        if inputState.jump:
            if self.grounded_time_remaining > 0:
                self.velocity.y = -800

        if inputState.right.pos_edge:
            self.facing_right = True
        elif inputState.left.pos_edge:
            self.facing_right = False

        target_speed = 400 * (int(inputState.right) - int(inputState.left))
        if abs(self.velocity.x - target_speed) < 10:
            self.velocity.x = target_speed
        else:
            self.velocity.x += (target_speed - self.velocity.x) * dt * 6

        if inputState.boost.pos_edge:
            self.explosion_timer = 0
            self.velocity.y -= 2200
            self.explosion_rect = self.rect

    def update(self, dt, blocks):
        target_speed = 1500
        if abs(self.velocity.y - target_speed) < 10:
            self.velocity.y = target_speed
        else:
            self.velocity.y += (target_speed - self.velocity.y) * dt * 1.4

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
                    self.grounded_time_remaining = 0.1
                else: # self.velocity.y is negative
                    self.rect.top = block.rect.bottom
                self.velocity.y = 0

        if self.grounded_time_remaining > 0:
            self.grounded_time_remaining -= dt

    def getSprite(self):
        sprites = self.sprites_right if self.facing_right else self.sprites_left
        animationLength = 8
        if -50 < self.velocity.x < 50:
            return sprites[0]
        sprite = sprites[self.animation_timer//animationLength]
        self.animation_timer += 1
        self.animation_timer %= animationLength*len(sprites)
        return sprite


    def draw(self, surface: Surface):
        surface.blit(self.getSprite(), self.rect)
        if self.explosion_timer >= 0:
            if self.explosion_timer >= 4*len(self.explosion_sprites):
                self.explosion_timer = -1
            else:
                surface.blit(self.explosion_sprites[self.explosion_timer//4], self.explosion_rect)
                self.explosion_timer += 1
