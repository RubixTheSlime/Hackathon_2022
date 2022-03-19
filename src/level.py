import pygame
from pygame.math import Vector2
from pygame.surface import Surface
import re

from backgroundblock import BackgroundBlock
from block import Block, BlockType


class Level:
    def __init__(self):
        self.background_sprite = pygame.image.load('src/res/BackgroundBlock/BackgroundBlock.png').convert()
        self.background_blocks: 'list[BackgroundBlock]' = []
        self.blocks: 'list[Block]' = []
        self.bombs = 0
        self.start = None
        self.level = 0

    def read(self, filename: str) -> None:
        self.level = int(re.search(r'\d+', filename).group())

        self.background_blocks = []
        if self.level < 10:
            for row in range(9):
                for col in range(4, 12):
                    self.background_blocks.append(BackgroundBlock(col, row))

        self.blocks = []
        with open(filename, 'r') as f:
            row = 0
            for line in f.readlines():
                if line.startswith('bombs:'):
                    self.bombs = int(line[6:])
                    continue
                for col, symbol in enumerate(line):
                    if symbol == '#':
                        self.blocks.append(Block(col, row, BlockType.NORMAL))
                    if symbol == 'X':
                        self.blocks.append(Block(col, row, BlockType.DEATH))
                    if symbol == '~':
                        self.blocks.append(Block(col, row, BlockType.FRAGILE))
                    if symbol == '_':
                        self.blocks.append(Block(col, row, BlockType.SEMISOLID))
                    if symbol == 'S':
                        self.start = Vector2(col, row)
                row += 1

    def copy_from(self, other: 'Level'):
        self.blocks = [Block(copy_from=block) for block in other.blocks]
        self.background_blocks = [BackgroundBlock(copy_from=block) for block in other.background_blocks]
        self.start = other.start
        self.level = other.level
        self.bombs = other.bombs

    def draw(self, surface: Surface) -> None:
        for block in self.background_blocks:
            block.draw(surface)
        for i, block in enumerate(self.blocks):
            block.draw(surface)
