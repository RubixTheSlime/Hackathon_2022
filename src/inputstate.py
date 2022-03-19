from dataclasses import dataclass

import pygame
from pygame.event import Event


class Button:
    def __init__(self):
        self.future = False
        self.state = False
        self.prev = False

    def set(self, state):
        self.future = state

    def advance(self):
        self.prev, self.state = self.state, self.future

    @property
    def pos_edge(self):
        return self.state and not self.prev

    @property
    def neg_edge(self):
        return not self.state and self.prev

    @property
    def on(self):
        return self.state

    def __bool__(self):
        return self.state

    def __int__(self):
        return int(self.state)


class InputState:
    def __init__(self):
        self.state = {name: Button() for name in (
            'down',
            'left',
            'right',
            'jump',
            'boost',
            'quit',
        )}

    def __getattr__(self, item):
        if item in self.state:
            return self.state[item]
        return False

    def flush(self):
        for button in self.state.values():
            button.advance()


def update_input_state(input_state: InputState, event: Event):
    try:
        button = {
            pygame.K_w: 'jump',
            pygame.K_UP: 'jump',
            pygame.K_s: 'down',
            pygame.K_DOWN: 'down',
            pygame.K_a: 'left',
            pygame.K_LEFT: 'left',
            pygame.K_d: 'right',
            pygame.K_RIGHT: 'right',
            pygame.K_SPACE: 'jump',
            pygame.K_k: 'boost',
            pygame.K_c: 'boost',
            pygame.K_e: 'boost',
            pygame.K_ESCAPE: 'quit',
        }[event.key]

    except KeyError:
        # a key that we're not using, fail gracefully
        return

    input_state.state[button].set(event.type == pygame.KEYDOWN)

