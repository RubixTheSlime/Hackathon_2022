import math

import pygame
from pygame import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from block import BlockType, Block
from explosion import ExplosionHandler
from inputstate import InputState


class Player:
    def __init__(self):
        self.has_landed = False
        self.grounded_time_remaining = 0
        self.animation_timer = 0
        self.has_won = False
        self.grenade_count = 0

        self.velocity = Vector2(0, 0)

        self.sprites_right = [pygame.image.load(f'src/res/Erik{x}.png').convert_alpha() for x in
                              ['', 'Left', '', 'Right']]
        self.sprites_left = [pygame.transform.flip(surface, True, False) for surface in self.sprites_right]
        self.facing_right = True

        self.rect = Rect((0, 0, 60, 110))
        self.draw_rect = self.sprites_right[0].get_rect()

        self.touching = {
            'down': False,
            'left': False,
            'right': False,
        }

        self.alive = True

    def handle_movement(self, input_state: InputState, dt: float, explosion_handler: ExplosionHandler) -> None:
        if input_state.jump:
            if self.touching['down'] and self.has_landed:
                self.velocity.y = -1000
                self.has_landed = False

        if input_state.right.pos_edge:
            self.facing_right = True
        elif input_state.left.pos_edge:
            self.facing_right = False

        target_speed = 400 * (int(input_state.right) - int(input_state.left))
        if abs(self.velocity.x - target_speed) < 10:
            self.velocity.x = target_speed
        else:
            self.velocity.x += (target_speed - self.velocity.x) * dt * 6

        if input_state.boost.pos_edge and self.grenade_count > 0:
            self.velocity.y -= 1600
            self.has_landed = False
            self.grenade_count -= 1
            explosion_handler.trigger_explosion(self.rect.centerx, self.rect.bottom)

    def update(self, dt: float, blocks: 'list[Block]') -> None:
        wall_sliding = self.touching['left'] or self.touching['right'] and self.velocity.y > 0
        target_speed = 300 if wall_sliding else 1500
        gravity_strength = 5 if wall_sliding else 1.4
        if abs(self.velocity.y - target_speed) < 10:
            self.velocity.y = target_speed
        else:
            self.velocity.y += (target_speed - self.velocity.y) * (1 - math.exp(-dt * gravity_strength))

        self.rect = self.rect.move((self.velocity.x * dt, 0))
        # detect x collision with blocks
        for block in blocks:
            if self.rect.colliderect(block.rect) and block.block_type != BlockType.SEMISOLID:
                if block.block_type == BlockType.DEATH:
                    self.kill()
                if self.velocity.x > 0:
                    self.rect.right = block.rect.left
                else:  # self.velocity.x is negative
                    self.rect.left = block.rect.right
                self.velocity.x = 0

        prev = self.rect
        self.rect = self.rect.move((0, self.velocity.y * dt))
        # detect y collision with blocks
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if block.block_type != BlockType.SEMISOLID:
                    if block.block_type == BlockType.DEATH:
                        self.kill()
                    if self.velocity.y >= 0:
                        self.rect.bottom = block.rect.top
                        self.has_landed = True
                    else:  # self.velocity.y is negative
                        self.rect.top = block.rect.bottom
                    self.velocity.y = 0
                else:
                    if prev.bottom <= block.rect.top < self.rect.bottom:
                        self.rect.bottom = block.rect.top
                        self.has_landed = True
                        self.velocity.y = 0

        # detect touches
        for offset, name, vertical in (
                ((20, 0), 'right', False),
                ((-20, 0), 'left', False),
                ((0, 20), 'down', True),
        ):
            self.touching[name] = False
            collision = Rect(Vector2(self.rect.topleft) + Vector2(offset), (self.rect.width, self.rect.height))
            for block in blocks:
                if block.block_type == BlockType.SEMISOLID and not vertical:
                    continue
                if collision.colliderect(block.rect):
                    self.touching[name] = True
                    break

        if self.grounded_time_remaining > 0:
            self.grounded_time_remaining -= dt

        # detect if dead
        if self.rect.y > 1080:
            self.kill()

        if self.rect.y <= 0:
            self.has_won = True

    def kill(self) -> None:
        self.alive = False

    def get_sprite(self) -> Surface:
        sprites = self.sprites_right if self.facing_right else self.sprites_left
        animation_length = 6
        if -50 < self.velocity.x < 50:
            return sprites[0]
        sprite = sprites[self.animation_timer // animation_length]
        self.animation_timer += 1
        self.animation_timer %= animation_length * len(sprites)
        return sprite

    def draw(self, surface: Surface):
        self.draw_rect.centerx = self.rect.centerx
        self.draw_rect.bottom = self.rect.bottom
        surface.blit(self.get_sprite(), self.draw_rect)

    def reset(self):
        self.grounded_time_remaining = 0
        self.animation_timer = 0

        self.velocity = Vector2(0, 0)
        self.alive = True
        self.has_won = False
