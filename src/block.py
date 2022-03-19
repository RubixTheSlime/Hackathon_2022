from enum import Enum

import pygame
from pygame import Surface


class BlockType(Enum):
    NORMAL = 1
    DEATH = 2
    FRAGILE = 3
    SEMISOLID = 4


class Block:
    block_type_name = {
        BlockType.NORMAL: "Block",
        BlockType.DEATH: "DeathBlock",
        BlockType.FRAGILE: "BreakableBlock",
        BlockType.SEMISOLID: "SemiSolid",
    }

    SIZE = 120

    def __init__(self, left, top, block_type: BlockType):
        self.block_type = block_type
        self.sprite = pygame.image.load(f'src/res/{Block.block_type_name[block_type]}.png').convert()
        self.rect = self.sprite.get_rect(left=left * Block.SIZE, top=top * Block.SIZE, width=Block.SIZE,
                                         height=Block.SIZE)

    def update(self):
        pass

    def draw(self, surface: Surface):
        surface.blit(self.sprite, self.rect)
