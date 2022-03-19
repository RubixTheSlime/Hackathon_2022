import pygame
from pygame import Vector2
from pygame import Surface


class Block:
    SIZE = 120

    def __init__(self, left, top, instant_death: bool = False, fragile: bool = False):
        self.instant_death = instant_death
        self.fragile = fragile
        self.sprite = pygame.image.load(f'src/res/{"Death" if instant_death else "Breakable" if fragile else ""}Block.png').convert()
        self.rect = self.sprite.get_rect(left=left * Block.SIZE, top=top * Block.SIZE, width=Block.SIZE,
                                         height=Block.SIZE)

    # This code was unused, but saved for if we want to try to make blocks breakable
    # def checkIfBroken(self, playerX, playerY):
    #     if self.fragile and playerY > self.rect.top and playerY < self.rect.top + 30 and playerX > self.rect.left and playerX < self.rect.left + Block.SIZE:
    #         print("Break!")

    def update(self):
        pass

    def draw(self, surface: Surface):
        surface.blit(self.sprite, self.rect)
