import pygame
from pygame.font import Font
from pygame.surface import Surface

from explosion import ExplosionHandler
from inputstate import InputState, update_input_state
from level import Level
from player import Player
from res.dims import dims
from res.string import strings

frame = 0


class Game:
    def __init__(self):
        pygame.init()
        self.input_state = InputState()
        self.running: bool = False
        self.window_surface: Surface = pygame.display.set_mode(
            (dims['window_width'], dims['window_height']))
        self.base_font: Font = None
        self.player = Player()
        self.level = Level()
        self.level_num: int = 0
        self.transition_frame: int = -1
        self.explosion_handler = ExplosionHandler()

        self.backgrounds: 'list[Surface]' = [pygame.image.load(f'src/res/{name}.png').convert() for name in
                                             ['StoryBackground', 'DayBackground', 'EveningBackground',
                                              'NightBackground', 'TheEnd']]
        self.start_level(0)

    def run(self) -> None:
        self.base_font = Font(None, dims['default_font_size'])
        pygame.display.set_caption(strings['window_title'])
        clock = pygame.time.Clock()

        self.running = True

        while self.running:
            dt = 1 / dims['fps']
            self.handle_events(dt)
            if self.input_state.quit:
                self.stop()
            self.update(dt)
            self.draw(dt)
            clock.tick(dims['fps'])

        pygame.quit()

    def stop(self) -> None:
        self.running = False

    def update(self, dt: float) -> None:
        if self.level_num == 0 and self.input_state.jump:
            self.start_level(1)
        if not self.player.alive:
            self.start_level()
        if self.level.blocks is not None:
            self.player.update(dt, self.level.blocks)
            self.explosion_handler.update(dt, self.level.blocks)
        if self.player.has_won and self.level_num < 10:
            self.start_transition()
            self.level_num += 1
            self.start_level(self.level_num)

    def start_level(self, level_num: int = None) -> None:
        if level_num is not None:
            self.level_num = level_num
        self.explosion_handler.clear()
        self.level.read(f'src/res/levels/level_{max(self.level_num, 1)}.txt')
        self.player.grenade_count = self.level.bombs
        self.player.rect.x, self.player.rect.y = self.level.start * 120
        self.player.reset()

    def handle_events(self, dt: float) -> None:
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

        if self.transition_frame != -1 and self.input_state.jump.pos_edge:
            self.transition_frame = -1
        elif not self.level_num == 0:
            if self.input_state.restart.pos_edge:
                self.start_level(self.level_num)
            self.player.handle_movement(self.input_state, dt, self.explosion_handler)

    def get_background_image(self, level_num: int) -> Surface:
        # return self.backgrounds[level_num]
        background = self.backgrounds[0]
        if 1 <= level_num <= 3:
            background = self.backgrounds[1]
        elif 4 <= level_num <= 6:
            background = self.backgrounds[2]
        elif 7 <= level_num <= 9:
            background = self.backgrounds[3]
        elif level_num == 10:
            background = self.backgrounds[4]
        return background

    def start_transition(self) -> None:
        self.transition_frame = 0

    def draw(self, dt: float) -> None:
        if self.transition_frame == -1:
            self.window_surface.blit(self.get_background_image(self.level_num), (0, 0))

            if not self.level_num == 0:
                self.level.draw(self.window_surface)
                self.window_surface.blit(self.base_font.render(f'Bombs - {self.player.grenade_count}', True, (0, 0, 0)),
                                         (50, 40))
                self.player.draw(self.window_surface)
                self.explosion_handler.draw(self.window_surface)
        else:
            if self.transition_frame >= 120:
                self.transition_frame = -1
            else:
                self.transition_frame += 1
                self.window_surface.fill((52, 89, 153))
                self.window_surface.blit(
                    self.base_font.render(f'Finished level {self.level_num}!', True, (255, 255, 255)),
                    (-60 + self.transition_frame, dims['window_height'] - 200))
        pygame.display.flip()
