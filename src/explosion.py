from math import ceil

import pygame
from pygame.rect import Rect
from pygame.surface import Surface


class ExplosionHandler:
    def __init__(self):
        self.explosions: 'list[Explosion]' = []

    def trigger_explosion(self, x, y):
        self.explosions.append(Explosion(x, y))

    def update(self, dt, blocks):
        for explosion in self.explosions:
            explosion.update(dt, blocks)
            if explosion.cull:
                self.explosions.remove(explosion)

    def draw(self, surface):
        for explosion in self.explosions:
            explosion.draw(surface)

    def clear(self):
        self.explosions.clear()


class Explosion:
    def __init__(self, x, y):
        self.sprites = [pygame.image.load(f'src/res/Explode{i}.png').convert_alpha() for i in range(1, 7)]
        self.rect: Rect = self.sprites[0].get_rect()
        self.rect.centerx, self.rect.centery = x, y
        self.cull = False
        self.end_time = len(self.sprites)
        self.timer = 0.0

    def update(self, dt, blocks):
        self.timer += dt*15
        self.cull = self.timer >= self.end_time
        collision_rect = Rect(0, 0, self.rect.width * self.timer / self.end_time, self.rect.height * self.timer / self.end_time)
        collision_rect.centerx, collision_rect.centery = self.rect.centerx, self.rect.centery
        for block in blocks:
            if collision_rect.colliderect(block.rect) and block.fragile:
                blocks.remove(block)

    def draw(self, surface: Surface):
        if not self.cull:
            surface.blit(self.sprites[int(self.timer)], self.rect)

