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

    def scale(self, dimension):
        return self.UNIT * dimension

    def draw_borders(self):
        # Main ellipse
        pygame.draw.ellipse(self.surface, BORDER_COLOUR, LocalRect(self.surface.get_rect()).resize(self.scale(85), self.scale(61)), int(self.scale(1)))

        # Left score
        rect = LocalRect(self.surface.get_rect()).resize(self.scale(15), self.scale(10)).move(self.scale(-41), 0)
        pygame.draw.rect(self.surface, BORDER_COLOUR, rect,0, int(self.scale(1)))
        pygame.draw.rect(self.surface, BACKGROUND_COLOUR, rect.inflate(self.scale(-1), self.scale(-1)), 0, int(self.scale(1)))

        # Right score
        rect = LocalRect(self.surface.get_rect()).resize(self.scale(15), self.scale(10)).move(+self.scale(41), 0)
        pygame.draw.rect(self.surface, BORDER_COLOUR, rect,0, int(self.scale(1)))
        pygame.draw.rect(self.surface, BACKGROUND_COLOUR, rect.inflate(self.scale(-1), self.scale(-1)), 0, int(self.scale(1)))

        # Inner border
        rect = LocalRect(self.surface.get_rect()).resize(self.scale(self.inner_border_width), self.scale(self.inner_border_height))
        pygame.draw.rect(self.surface, BORDER_COLOUR, rect, 0, int(self.scale(1)))
        pygame.draw.rect(self.surface, BACKGROUND_COLOUR, rect.inflate(self.scale(-1), self.scale(-1)), 0, int(self.scale(1)))

    def draw_score(self, score, x, y):
        rect = LocalRect(self.surface.get_rect().move(self.scale(x), self.scale(y))).resize(self.scale(13),self.scale(8))
        pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR, rect, 0, int(self.scale(1)))
        self.draw_text(str(score), rect.resize(rect.width, int(self.scale(6.4))))

    def draw_hidden_answer(self, cell, i):
        pygame.draw.ellipse(self.surface, TEXT_BACKGROUND_COLOUR + '4', cell.resize(self.scale(8), self.scale(6)))
        self.draw_text(str(i + 1), cell.resize(self.scale(24), self.scale(6.4)), "fonts/NimbusSans-Bold.otf")

    def draw_revealed_answer(self, cell, answer_text, answer_score):
        tmp = cell.inflate(self.scale(-1), self.scale(-1))
        answer_rect, score_rect = tmp.split_h(self.scale(-5))
        pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR + '4', answer_rect, 0, int(self.scale(1/2)))
        pygame.draw.rect(self.surface, 'white', answer_rect, int(self.scale(1/5)), int(self.scale(1/2)))
        self.draw_text(answer_text.upper(), answer_rect.resize(answer_rect.width - self.scale(1), int(self.scale(3.5))), "fonts/NimbusSans-Bold.otf")
        self.draw_text(str(answer_score), score_rect.resize(score_rect.width,self.scale(4)), "fonts/NimbusSansNarrow-Bold.otf")

    def draw_answer_grid(self):
        area = LocalRect(self.surface.get_rect())
        area.resize_ip(self.scale(self.inner_border_width - 2), self.scale(self.inner_border_height - 2))

        i = 0
        for column in area.columns(2):
            for cell in column.rows(4):
                pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR, cell.inflate(self.scale(-1/2), self.scale(-1/2)), 0, int(self.scale(1/2)))
                if i < self.model.get_answer_count():
                    if self.model.is_revealed_answer(i):
                        self.draw_revealed_answer(cell, self.model.get_answer_text(i), self.model.get_answer_score(i))
                    else:
                        self.draw_hidden_answer(cell, i)
                i += 1

    def draw_strike(self, count):
        for rect in LocalRect(self.surface.get_rect()).resize(self.scale(32) * count,self.scale(32)).columns(count):
            pygame.draw.rect(self.surface, "black", rect.resize(self.scale(34),self.scale(34)), 0, int(self.scale(3)))
            pygame.draw.rect(self.surface, "red", rect.resize(self.scale(30),self.scale(30)), int(self.scale(4)), int(self.scale(2)))
            font = pygame.font.Font("fonts/NimbusSans-Regular.otf", int(self.scale(47)))
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

