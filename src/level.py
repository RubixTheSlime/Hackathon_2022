from pygame.math import Vector2
from pygame.surface import Surface

from Block import Block


class Level:
    def __init__(self):
        self.blocks: 'list[Block]' = None
        self.bombs = 0
        self.start = None

    def read(self, filename: str):
        self.blocks = []
        with open(filename, 'r') as f:
            for row, line in enumerate(f.readlines()):
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
                    if symbol == 'S':
                        self.start = Vector2(col, row)

    def draw(self, surface: Surface):
        for i, block in enumerate(self.blocks):
            block.draw(surface)
