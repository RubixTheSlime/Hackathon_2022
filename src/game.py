from time import sleep
import pygame
from pygame.font import Font
from pygame.surface import Surface
from BackgroundBlock import BackgroundBlock

from inputstate import InputState, update_input_state
from level import Level
from res.dims import dims
from res.string import strings
from player import Player

from Block import Block

frame = 0

class Game:
    def __init__(self):
        pygame.init()
        self.input_state = InputState()
        self.running: bool = False
        self.window_surface = pygame.display.set_mode((dims['window_width'], dims['window_height']))
        self.base_font: Font = None
        self.player = Player()
        self.level = Level()
        self.level.read('src/res/levels/test_level_2.txt')
        # self.blocks: 'list[Block]' = [ Block(left=i, top=dims['window_height']/Block.SIZE - 1) for i in range(16) ] + [ Block(left=i, top=dims['window_height']/Block.SIZE - 2) for i in range(6,10)]
        self.backgrounds = [ pygame.image.load(f'src/res/{name}.png').convert() for name in ['StoryBackground', 'DayBackground', 'EveningBackground', 'NightBackground', 'TheEnd' ] ]
        self.levelNum = 0

    def run(self) -> None:
        self.base_font = Font(None, dims['default_font_size'])
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
        if not self.player.alive:
            self.levelNum = 0
        self.player.update(dt, self.level.blocks)
        if self.player.hasWon:
            # Won Level
            self.levelNum += 1

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
            self.level.draw(self.window_surface)
            self.window_surface.blit(self.base_font.render(f'Bombs - {self.player.grenade_count}', True, (0, 0, 0)), (50, 50))
            self.player.draw(self.window_surface)
        pygame.display.flip()