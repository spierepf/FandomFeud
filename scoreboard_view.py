import pygame

from pygame_view import PygameView
from config import BORDER_COLOUR, BACKGROUND_COLOUR, TEXT_BACKGROUND_COLOUR, BELL_SOUND, BUZZER_SOUND
from rect_builder import RectBuilder
from side import Side


class ScoreboardView(PygameView):
    def __init__(self, model, surface):
        super().__init__(model, surface)

    def draw_text(self, text, x, y, height, width=None, font_name="fonts/NimbusSans-Regular.otf"):
        font = pygame.font.Font(font_name, int(self.UNIT * height))
        shadow = font.render(text, True, "black")
        foreground = font.render(text, True, "white")
        if width is not None and width * self.UNIT < shadow.get_width():
            shadow = pygame.transform.scale(shadow, (width * self.UNIT, shadow.get_height()))
            foreground = pygame.transform.scale(foreground, (width * self.UNIT, shadow.get_height()))
        self.surface.blit(shadow, RectBuilder(self.surface, shadow.get_rect()).translate(x + 0.3, y + 0.3).unscaled_translate(0, (font.get_linesize() - font.get_height()) / 2).done())
        self.surface.blit(foreground, RectBuilder(self.surface, foreground.get_rect()).translate(x, y).unscaled_translate(0, (font.get_linesize() - font.get_height()) / 2).done())

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
        pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR,
                         RectBuilder(self.surface).size(13, 8).translate(x, y).done(), 0, int(self.UNIT))
        self.draw_text(str(score), x, y, 6.4)

    def draw_hidden_answer(self, x, y, i):
        pygame.draw.ellipse(self.surface, TEXT_BACKGROUND_COLOUR + '4',
                            RectBuilder(self.surface).size(24, 8).translate(x, y).size(8, 6).done())
        self.draw_text(str(i+1), x, y, 6.4, 24, "fonts/NimbusSans-Bold.otf")

    def draw_revealed_answer(self, x, y, answer_text, answer_score):
        score_width = 5
        answer_width = self.box_width - 1 - score_width
        answer_height = self.box_height - 1
        pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR + '4',
                         RectBuilder(self.surface).size(answer_width, answer_height).translate(x-score_width/2, y).done(), 0,
                         int(self.UNIT / 2))
        pygame.draw.rect(self.surface, 'white',
                         RectBuilder(self.surface).size(answer_width, answer_height).translate(x-score_width/2, y).done(),
                         int(self.UNIT / 5), int(self.UNIT / 2))
        self.draw_text(answer_text.upper(), x - score_width/2, y,  3.5, answer_width-1, "fonts/NimbusSans-Bold.otf")
        self.draw_text(str(answer_score), x + ((self.box_width-1)/2) - (score_width/2), y, 4, score_width,"fonts/NimbusSansNarrow-Bold.otf")

    def draw_answer_grid(self):
        for col in range(2):
            for row in range(4):
                x = (col - 0.5) * self.box_width
                y = (row - 1.5) * self.box_height
                i = col * 4 + row
                pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR,
                                 RectBuilder(self.surface).size(self.box_width-0.5, self.box_height-0.5).translate(x, y).done(),
                                 0, int(self.UNIT / 2))
                if i < self.model.get_answer_count():
                    if self.model.is_revealed_answer(i):
                        self.draw_revealed_answer(x, y, self.model.get_answer_text(i), self.model.get_answer_score(i))
                    else:
                        self.draw_hidden_answer(x, y, i)

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

