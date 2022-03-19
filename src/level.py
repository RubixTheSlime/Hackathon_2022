import pygame
from pygame.math import Vector2
from pygame.surface import Surface

from Block import Block


class Level:
    def __init__(self):
        self.background_sprite = pygame.image.load('src/res/BackgroundBlock.png').convert()
        self.blocks: 'list[Block]' = None
        self.bombs = 0
        self.start = None
        self.level = 0

    def read(self, filename: str):
        self.level = int(filename.strip('.txt')[-1])
        self.blocks = []
        with open(filename, 'r') as f:
            row = 0
            for line in f.readlines():
                if line.startswith('bombs:'):
                    self.bombs = int(line[6:])
                    continue
                for col, symbol in enumerate(line):
                    if symbol == '#':
                        self.blocks.append(Block(col, row))
                    if symbol == 'X':
                        self.blocks.append(Block(col, row, instant_death=True))
                    if symbol == '~':
                        self.blocks.append(Block(col, row, fragile=True))
                    if symbol == '_':
                        self.blocks.append(Block(col, row, semisolid=True))
                    if symbol == 'S':
                        self.start = Vector2(col, row)
                row += 1

    def draw(self, surface: Surface):
        if self.level < 4:
            for row in range(9):
                for col in range(8):
                    surface.blit(self.background_sprite, ((col+4)*Block.SIZE, row*Block.SIZE))
        for i, block in enumerate(self.blocks):
            block.draw(surface)
