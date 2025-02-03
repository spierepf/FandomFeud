import pygame

from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '..')))
from core.pygame_view import PygameView
from core.config import BORDER_COLOUR, BACKGROUND_COLOUR, TEXT_BACKGROUND_COLOUR, BELL_SOUND, BUZZER_SOUND
from core.rect_builder import RectBuilder
from core.side import Side

class LocalRect(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def resize(self, new_width, new_height):
        return self.inflate(new_width - self.width, new_height - self.height)

    def resize_ip(self, new_width, new_height):
        self.inflate_ip(new_width - self.width, new_height - self.height)

    def columns(self, n):
        width = self.width / n
        for i in range(n):
            yield LocalRect(self.left + i*width, self.top, width, self.height)

    def rows(self, n):
        height = self.height / n
        for i in range(n):
            yield LocalRect(self.left, self.top + i*height, self.width, height)

    def split_h(self, width):
        if width < 0:
            return (
                LocalRect(self.left, self.top, self.width + width, self.height),
                LocalRect(self.left + (self.width + width), self.top, -width, self.height)
            )
        else:
            return (
                LocalRect(self.left, self.top, width, self.height),
                LocalRect(self.left + width, self.top, self.width-width, self.height)
            )

class ScoreboardView(PygameView):
    def __init__(self, model, surface):
        super().__init__(model, surface)
        self.inner_border_width = 61
        self.inner_border_height = 38
        self.box_width = (self.inner_border_width - 2) / 2
        self.box_height = (self.inner_border_height - 2) / 4

    def draw_text(self, text, rect, font_name="fonts/NimbusSans-Regular.otf"):
        font = pygame.font.Font(font_name, int(rect.height))
        shadow = font.render(text, True, "black")
        foreground = font.render(text, True, "white")
        if rect.width < shadow.get_width():
            shadow = pygame.transform.scale(shadow, (rect.width, shadow.get_height()))
            foreground = pygame.transform.scale(foreground, (rect.width, shadow.get_height()))
        tmp = rect.resize(foreground.get_width(), foreground.get_height()).move(0, (font.get_linesize() - font.get_height()) / 2)
        self.surface.blit(shadow, tmp.move(int(self.UNIT*0.3), int(self.UNIT*0.3)))
        self.surface.blit(foreground, tmp)

    def draw_borders(self):
        # Main ellipse
        pygame.draw.ellipse(self.surface, BORDER_COLOUR, RectBuilder(self.surface).size(85, 61).done(), int(self.UNIT))
        # pygame.draw.ellipse(self.surface, BACKGROUND_COLOUR, RectBuilder(self.surface).size(84, 60).done())

        # Left score
        pygame.draw.rect(self.surface, BORDER_COLOUR, RectBuilder(self.surface).size(15, 10).translate(-41, 0).done(),
                         0, int(self.UNIT))
        pygame.draw.rect(self.surface, BACKGROUND_COLOUR,
                         RectBuilder(self.surface).size(14, 9).translate(-41, 0).done(), 0, int(self.UNIT))

        # Right score
        pygame.draw.rect(self.surface, BORDER_COLOUR, RectBuilder(self.surface).size(15, 10).translate(+41, 0).done(),
                         0, int(self.UNIT))
        pygame.draw.rect(self.surface, BACKGROUND_COLOUR,
                         RectBuilder(self.surface).size(14, 9).translate(+41, 0).done(), 0, int(self.UNIT))

        # Inner border
        pygame.draw.rect(self.surface, BORDER_COLOUR, RectBuilder(self.surface).size(self.inner_border_width, self.inner_border_height).done(), 0,
                         int(self.UNIT))
        pygame.draw.rect(self.surface, BACKGROUND_COLOUR, RectBuilder(self.surface).size(self.inner_border_width - 1, self.inner_border_height - 1).done(), 0,
                         int(self.UNIT))

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

    def draw_x(self, count):
        for i in range(count):
            x = 32 * (i - 0.5 * count + 0.5)
            pygame.draw.rect(self.surface, "black", RectBuilder(self.surface).size(34, 34).translate(x, 0).done(), 0,
                             int(self.UNIT * 3))
            pygame.draw.rect(self.surface, "red", RectBuilder(self.surface).size(30, 30).translate(x, 0).done(),
                             int(4 * self.UNIT),
                             int(self.UNIT * 2))
            font = pygame.font.Font("fonts/NimbusSans-Regular.otf", int(self.UNIT * 47))
            shadow = font.render("\u00D7", True, "red")
            self.surface.blit(shadow, RectBuilder(self.surface, shadow.get_rect()).translate(x, 0).done())

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
                self.draw_x(self.model.get_strike())
            else:
                self.model.clear_strike()

