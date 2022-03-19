import pygame
from pygame.font import Font
from pygame.surface import Surface

from res.dims import dims
from res.string import strings
from src.player import Player


class Game:
    def __init__(self):
        self.running: bool = None
        self.window_surface: Surface = None
        self.base_font: Font = None
        self.player = Player()

    def run(self) -> None:
        pygame.init()
        self.base_font = Font(None, dims['default_font_size'])
        self.window_surface = pygame.display.set_mode((dims['window_width'], dims['window_height']))
        pygame.display.set_caption(strings['window_title'])
        clock = pygame.time.Clock()

        self.running = True

        while self.running:
            self.handle_events()
            self.update(1/30)
            self.draw()
            clock.tick(dims['fps'])

    def stop(self):
        self.running = False

    def update(self, dt):
        self.player.update(dt)

    def handle_events(self):
        for event in pygame.event.get():
            try:
                {
                    pygame.QUIT: self.stop,
                }[event.type]()
            except KeyError:
                pass

    def draw(self):
        self.window_surface.fill((255, 255, 255), self.window_surface.get_rect())
        self.player.draw(self.window_surface)
        pygame.display.flip()
