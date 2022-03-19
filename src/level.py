from pygame.surface import Surface

from Block import Block


class Level:
    def __init__(self):
        self.blocks: 'list[Block]' = None

    def read(self, filename: str):
        self.blocks = []
        with open(filename, 'r') as f:
            for row, line in enumerate(f.readlines()):
                for col, symbol in enumerate(line):
                    if symbol == '#':
                        self.blocks.append(Block(col, row))
                    if symbol == 'X':
                        self.blocks.append(Block(col, row, instant_death=True))
                    if symbol == '~':
                        self.blocks.append(Block(col, row, fragile=True))

    def draw(self, surface: Surface):
        for i, block in enumerate(self.blocks):
            block.draw(surface)
