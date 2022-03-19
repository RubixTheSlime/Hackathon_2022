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
            self.rect = Rect(copy_from.rect)
            self.flip_x, self.flip_y = copy_from.flip_x, copy_from.flip_y
            self.sprite = pygame.transform.flip(pygame.image.load(self.path).convert(), self.flip_x, self.flip_y)
            return
        self.flip_x = self.flip_y = False
        if block_type in (BlockType.NORMAL, BlockType.FRAGILE, BlockType.SEMISOLID):
            self.flip_x = random.randint(0, 1)
        if block_type in (BlockType.NORMAL, BlockType.FRAGILE):
            self.flip_y = random.randint(0, 1)

        self.block_type = block_type
        path_start = f'src/res/{Block.block_type_name[block_type]}'
        self.path = os.path.join(path_start, random.choice(os.listdir(path_start)))
        self.sprite = pygame.transform.flip(pygame.image.load(self.path).convert(), self.flip_x, self.flip_y)
        self.rect = self.sprite.get_rect(left=left * Block.SIZE, top=top * Block.SIZE, width=Block.SIZE,
                                         height=Block.SIZE)

    def update(self):
        pass

    def draw(self, surface: Surface):
        surface.blit(self.sprite, self.rect)
