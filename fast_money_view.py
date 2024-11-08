import pygame

from config import BORDER_COLOUR, BACKGROUND_COLOUR, TEXT_BACKGROUND_COLOUR, BELL_SOUND, BUZZER_SOUND, DUPLICATE_SOUND
from rect_builder import RectBuilder
from side import Side


class FastMoneyView:
    def __init__(self, model, surface, fullscreen):
        self.bg = pygame.image.load("FamilyFeud_PurpleBG.jpg")
        if fullscreen:
            self.bg = pygame.transform.scale_by(self.bg, 2)
        self.model = model
        self.surface = surface
        self.UNIT = min(surface.get_width() / 100, surface.get_height() / 75)
        self.inner_border_width = 61
        self.inner_border_height = 38
        self.box_width = (self.inner_border_width - 2) / 2
        self.box_height = (self.inner_border_height - 2) / 4

    def draw_text(self, text, x, y, height, width=None, font_name="fonts/NimbusSans-Regular.otf"):
        font = pygame.font.Font(font_name, int(self.UNIT * height))
        shadow = font.render(text, True, "black")
        foreground = font.render(text, True, "white")
        if width is not None and width * self.UNIT < shadow.get_width():
            shadow = pygame.transform.scale(shadow, (width * self.UNIT, shadow.get_height()))
            foreground = pygame.transform.scale(foreground, (width * self.UNIT, shadow.get_height()))
        self.surface.blit(shadow, RectBuilder(self.surface, shadow.get_rect()).translate(x + 0.3, y + 0.3).unscaled_translate(0, (font.get_linesize() - font.get_height()) / 2).done())
        self.surface.blit(foreground, RectBuilder(self.surface, foreground.get_rect()).translate(x, y).unscaled_translate(0, (font.get_linesize() - font.get_height()) / 2).done())

    def draw(self):
        self.surface.blit(self.bg, (0, 0))

        pygame.draw.rect(self.surface, BORDER_COLOUR, RectBuilder(self.surface).size(88, 66).done(),
                         int(self.UNIT), int(self.UNIT))

        #print(self.model.get_timer_duration(), self.model.get_timer_end_time(), self.model.get_timer_start())
        if self.model.get_timer_start():
            self.model.set_timer_end_time(pygame.time.get_ticks() + 1000 * self.model.get_timer_duration())
            self.model.set_timer_start(False)
        if self.model.get_timer_end_time() is not None:
            if pygame.time.get_ticks() > self.model.get_timer_end_time():
                timer_time = 0
                self.model.set_timer_end_time(None)
                self.model.set_timer_duration(0)
            else:
                timer_time = int((self.model.get_timer_end_time() - pygame.time.get_ticks())/1000)
        else:
            timer_time = self.model.get_timer_duration()
        pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR, RectBuilder(self.surface).size(15, 11).translate(0, -25).done(),
                         0, int(self.UNIT))
        self.draw_text(str(timer_time), 0, -25, 10)

        if self.model.get_play_duplicate_sound():
            self.model.set_play_duplicate_sound(False)
            DUPLICATE_SOUND.play()

        total_score = 0
        for col in range(2):
            for row in range(5):
                index = col * 5 + row
                x = 42 * (col - 0.5)
                y = 8 * (row - 2.5) + 5
                pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR, RectBuilder(self.surface).size(33, 7).translate(x + 0.25 - 4, y + 0.25).done(), 0, int(self.UNIT))
                pygame.draw.rect(self.surface, 'black', RectBuilder(self.surface).size(33, 7).translate(x - 4, y).done(), 0, int(self.UNIT))
                if self.model.get_answer(index) is not None:
                    self.draw_text(self.model.get_answer(index).upper(), x - 4, y, 6, width=32)

                pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR, RectBuilder(self.surface).size(7, 7).translate(x + 0.25 + 16.5, y + 0.25).done(), 0, int(self.UNIT))
                pygame.draw.rect(self.surface, 'black', RectBuilder(self.surface).size(7, 7).translate(x + 16.5, y).done(), 0, int(self.UNIT))
                if self.model.get_score(index) is not None:
                    self.draw_text(str(self.model.get_score(index)), x + 16.5, y, 6)
                    total_score += self.model.get_score(index)
        x = -10
        y = 26
        pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR, RectBuilder(self.surface).size(50, 7).translate(x,y).done(), 0, int(self.UNIT))
        pygame.draw.rect(self.surface, 'black', RectBuilder(self.surface).size(50, 7).translate(x-0.25,y-0.25).done(), 0, int(self.UNIT))
        self.draw_text('GRAND TOTAL', x-0.25,y-0.25, 7)

        x += 31
        pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR, RectBuilder(self.surface).size(11, 7).translate(x,y).done(), 0, int(self.UNIT))
        pygame.draw.rect(self.surface, 'black', RectBuilder(self.surface).size(11, 7).translate(x-0.25,y-0.25).done(), 0, int(self.UNIT))
        self.draw_text(str(total_score), x - 0.25, y - 0.25, 7)
