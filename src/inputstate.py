from pygame.event import Event


class InputState:
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.jump = False

    def handle_event(self, event: Event):
        pass

