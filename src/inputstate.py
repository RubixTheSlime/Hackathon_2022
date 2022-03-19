import re

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
            'restart',
        )}

    def __getattr__(self, item):
        if item in self.state:
            return self.state[item]
        return False

    def flush(self):
        for button in self.state.values():
            button.advance()

    def handle_input_event(self, event: Event):
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
                pygame.K_r: 'restart',
            }[event.key]

        except KeyError:
            # a key that we're not using, fail gracefully
            return

        self.state[button].set(event.type == pygame.KEYDOWN)

    def handle_joystick_button_event(self, event: Event):
        try:
            button = {
                pygame.CONTROLLER_BUTTON_A: 'jump',
                pygame.CONTROLLER_BUTTON_B: 'boost',
                pygame.CONTROLLER_BUTTON_START: 'restart',
            }[event.button]
        except KeyError:
            return
        self.state[button].set(event.type == pygame.JOYBUTTONDOWN)

    def handle_joystick_hat_event(self, event: Event):
        print(event.value)
        self.state['right'].set(event.value[0] == 1)
        self.state['down'].set(event.value[1] == -1)
        self.state['left'].set(event.value[0] == -1)

