from time import sleep
import pygame
from pygame.font import Font
from pygame.surface import Surface

from inputstate import InputState, update_input_state
from res.dims import dims
from res.string import strings
from player import Player

from Block import Block


class Game:
    def __init__(self):
        self.input_state = InputState()
        self.running: bool = False
        self.window_surface: Surface = None
        self.background_image = pygame.image.load('src/res/DayBackground.png')
        self.base_font: Font = None
        self.player = Player()
        self.blocks: 'list[Block]' = [ Block(left=i*Block.SIZE, top=dims['window_height']-Block.SIZE) for i in range(16) ] + [ Block(left=i*Block.SIZE + 6*Block.SIZE, top=dims['window_height'] - Block.SIZE*2) for i in range(4)]
        self.backgrounds = [pygame.image.load('src/res/StoryBackground.png'), pygame.image.load('src/res/DayBackground.png'), pygame.image.load('src/res/EveningBackground.png'), pygame.image.load('src/res/NightBackground.png'), pygame.image.load('src/res/TheEnd.png')]
        self.levelNum = 0

    def run(self) -> None:
        pygame.init()
        self.base_font = Font(None, dims['default_font_size'])
        self.window_surface = pygame.display.set_mode((dims['window_width'], dims['window_height']))
        pygame.display.set_caption(strings['window_title'])
        clock = pygame.time.Clock()

        self.running = True

        while self.running:
            dt = 1/dims['fps']
            self.handle_events(dt)
            if self.input_state.quit:
                self.stop()
            self.update(dt)
            self.draw(dt)
            clock.tick(dims['fps'])

        pygame.quit()

    def stop(self):
        self.running = False

    def update(self, dt):
        if self.levelNum == 0 and self.input_state.jump:
            self.levelNum = 1
        self.player.update(dt, self.blocks)

    def handle_events(self, dt):
        for event in pygame.event.get():
            try:
                {
                    pygame.QUIT: self.stop,
                    pygame.KEYDOWN: lambda: update_input_state(self.input_state, event),
                    pygame.KEYUP: lambda: update_input_state(self.input_state, event),
                }[event.type]()
            except KeyError:
                pass

        self.input_state.flush()
        
        if not self.levelNum == 0:
            self.player.handle_movement(self.input_state, dt)

    def getBackgroundImage(self, levelNum):
        return self.backgrounds[levelNum]
    
    def draw(self, dt):
        self.window_surface.blit(self.getBackgroundImage(self.levelNum), (0,0))

        if not self.levelNum == 0:
            for i, block in enumerate(self.blocks):
                block.draw(self.window_surface)
            self.player.draw(self.window_surface)
        pygame.display.flip()
