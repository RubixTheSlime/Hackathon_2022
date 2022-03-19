import os
import random
from enum import Enum

import pygame
from pygame import Surface
from pygame.rect import Rect


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
        BlockType.SEMISOLID: "SemiSolidBlock",
    }

    SIZE = 120

    def __init__(self, left: int = None, top: int = None, block_type: BlockType = None, copy_from: 'Block' = None):
        if copy_from is not None:
            self.block_type = copy_from.block_type
            self.path = copy_from.path
            self.sprite = pygame.image.load(self.path).convert()
            self.rect = Rect(copy_from.rect)
            return
        self.block_type = block_type
        path_start = f'src/res/{Block.block_type_name[block_type]}'
        self.path = os.path.join(path_start, random.choice(os.listdir(path_start)))
        self.sprite = pygame.image.load(self.path).convert()
        self.rect = self.sprite.get_rect(left=left * Block.SIZE, top=top * Block.SIZE, width=Block.SIZE,
                                         height=Block.SIZE)

    def update(self):
        pass

    def draw(self, surface: Surface):
        surface.blit(self.sprite, self.rect)
