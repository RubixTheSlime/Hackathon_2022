from dataclasses import dataclass

import pygame
from pygame.event import Event


@dataclass
class InputState:
    def __init__(self):
        self.state = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'jump': False
        }

    def __getattr__(self, item):
        if item in self.state:
            return self.state[item]
        return False


def update_input_state(input_state: InputState, event: Event):
    try:
        button = {
            pygame.K_w: 'up',
            pygame.K_UP: 'up',
            pygame.K_s: 'down',
            pygame.K_DOWN: 'down',
            pygame.K_a: 'left',
            pygame.K_LEFT: 'left',
            pygame.K_d: 'right',
            pygame.K_RIGHT: 'right',
            pygame.K_SPACE: 'jump',
        }[event.key]

    except KeyError:
        # a key that we're not using, fail gracefully
        return

    input_state.state[button] = (event.type == pygame.KEYDOWN)