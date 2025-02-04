import pygame

from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '..')))
from core.pygame_view import PygameView
from core.local_rect import LocalRect
from core.config import BORDER_COLOUR, BACKGROUND_COLOUR, TEXT_BACKGROUND_COLOUR, BELL_SOUND, BUZZER_SOUND
from core.side import Side


class ScoreboardView(PygameView):
    def __init__(self, model, surface):
        super().__init__(model, surface)
        self.inner_border_width = 61
        self.inner_border_height = 38
        self.box_width = (self.inner_border_width - 2) / 2
        self.box_height = (self.inner_border_height - 2) / 4

    def draw_borders(self):
        # Main ellipse
        pygame.draw.ellipse(self.surface, BORDER_COLOUR, LocalRect(self.surface.get_rect()).resize(85*self.UNIT, 61*self.UNIT), int(self.UNIT))

        # Left score
        rect = LocalRect(self.surface.get_rect()).resize(15*self.UNIT, 10*self.UNIT).move(-41*self.UNIT, 0)
        pygame.draw.rect(self.surface, BORDER_COLOUR, rect,0, int(self.UNIT))
        pygame.draw.rect(self.surface, BACKGROUND_COLOUR, rect.inflate(-self.UNIT, -self.UNIT), 0, int(self.UNIT))

        # Right score
        rect = LocalRect(self.surface.get_rect()).resize(15*self.UNIT, 10*self.UNIT).move(+41*self.UNIT, 0)
        pygame.draw.rect(self.surface, BORDER_COLOUR, rect,0, int(self.UNIT))
        pygame.draw.rect(self.surface, BACKGROUND_COLOUR, rect.inflate(-self.UNIT, -self.UNIT), 0, int(self.UNIT))

        # Inner border
        rect = LocalRect(self.surface.get_rect()).resize(self.inner_border_width * self.UNIT, self.inner_border_height * self.UNIT)
        pygame.draw.rect(self.surface, BORDER_COLOUR, rect, 0, int(self.UNIT))
        pygame.draw.rect(self.surface, BACKGROUND_COLOUR, rect.inflate(-self.UNIT, -self.UNIT), 0, int(self.UNIT))

    def draw_score(self, score, x, y):
        rect = LocalRect(self.surface.get_rect().move(x * self.UNIT, y * self.UNIT)).resize(self.UNIT * 13, self.UNIT * 8)
        pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR, rect, 0, int(self.UNIT))
        self.draw_text(str(score), rect.resize(rect.width, int(6.4 * self.UNIT)))

    def draw_hidden_answer(self, cell, i):
        pygame.draw.ellipse(self.surface, TEXT_BACKGROUND_COLOUR + '4', cell.resize(8 * self.UNIT, 6 * self.UNIT))
        self.draw_text(str(i + 1), cell.resize(24 * self.UNIT, 6.4 * self.UNIT), "fonts/NimbusSans-Bold.otf")

    def draw_revealed_answer(self, cell, answer_text, answer_score):
        tmp = cell.inflate(-self.UNIT, -self.UNIT)
        answer_rect, score_rect = tmp.split_h(-5*self.UNIT)
        pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR + '4', answer_rect, 0, int(self.UNIT / 2))
        pygame.draw.rect(self.surface, 'white', answer_rect, int(self.UNIT / 5), int(self.UNIT / 2))
        self.draw_text(answer_text.upper(), answer_rect.resize(answer_rect.width - self.UNIT, int(self.UNIT * 3.5)), "fonts/NimbusSans-Bold.otf")
        self.draw_text(str(answer_score), score_rect.resize(score_rect.width, self.UNIT * 4), "fonts/NimbusSansNarrow-Bold.otf")

    def draw_answer_grid(self):
        area = LocalRect(self.surface.get_rect())
        area.resize_ip(self.UNIT * (self.inner_border_width - 2), self.UNIT * (self.inner_border_height - 2))

        i = 0
        for column in area.columns(2):
            for cell in column.rows(4):
                pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR, cell.inflate(-self.UNIT/2, -self.UNIT/2), 0, int(self.UNIT/2))
                if i < self.model.get_answer_count():
                    if self.model.is_revealed_answer(i):
                        self.draw_revealed_answer(cell, self.model.get_answer_text(i), self.model.get_answer_score(i))
                    else:
                        self.draw_hidden_answer(cell, i)
                i += 1

    def draw_strike(self, count):
        for rect in LocalRect(self.surface.get_rect()).resize(self.UNIT * 32 * count, self.UNIT * 32).columns(count):
            pygame.draw.rect(self.surface, "black", rect.resize(self.UNIT * 34, self.UNIT * 34), 0, int(self.UNIT * 3))
            pygame.draw.rect(self.surface, "red", rect.resize(self.UNIT * 30, self.UNIT * 30), int(4 * self.UNIT), int(self.UNIT * 2))
            font = pygame.font.Font("fonts/NimbusSans-Regular.otf", int(self.UNIT * 47))
            shadow = font.render("\u00D7", True, "red")
            self.surface.blit(shadow, rect.resize(shadow.get_width(), shadow.get_height()))

    def draw_scores(self):
        self.draw_score(self.model.get_score(Side.LEFT), -41, 0)  # left score
        self.draw_score(self.model.get_score(Side.RIGHT), +41, 0)  # right score
        self.draw_score(self.model.get_pot(), 0, -24)  # pot

    def draw(self):
        self.draw_background()
        self.draw_borders()
        self.draw_scores()
        self.draw_answer_grid()
        if self.model.is_newly_revealed():
            self.model.clear_newly_revealed()
            BELL_SOUND.play()

        if self.model.get_strike() is not None:
            if self.model.get_strike_start_time() is None:
                self.model.set_strike_start_time(pygame.time.get_ticks())
                BUZZER_SOUND.play()
            elif pygame.time.get_ticks() - self.model.get_strike_start_time() < int(BUZZER_SOUND.get_length() * 1000):
                self.draw_strike(self.model.get_strike())
            else:
                self.model.clear_strike()

