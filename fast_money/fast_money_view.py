import pygame

from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '..')))
from core.pygame_view import PygameView
from core.local_rect import LocalRect
from core.config import BORDER_COLOUR, TEXT_BACKGROUND_COLOUR, DUPLICATE_SOUND, POINTS_SOUND, NO_POINTS_SOUND, REVEAL_SOUND


class FastMoneyView(PygameView):
    def __init__(self, model, surface):
        super().__init__(model, surface)

    def draw_timer(self, timer_time):
        tmp = LocalRect(self.surface.get_rect()).resize(15 * self.UNIT, 11 * self.UNIT).move(0, -25 * self.UNIT)

        pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR, tmp,0, int(self.UNIT))
        self.draw_text(str(timer_time), tmp)

    def draw_shadow_box(self, rect):
        pygame.draw.rect(self.surface, TEXT_BACKGROUND_COLOUR, rect.move(int(self.UNIT / 4), int(self.UNIT / 4)), 0, int(self.UNIT))
        pygame.draw.rect(self.surface, 'black', rect, 0, int(self.UNIT))

    def draw(self):
        self.draw_background()

        pygame.draw.rect(self.surface, BORDER_COLOUR, LocalRect(self.surface.get_rect()).resize(88 * self.UNIT, 66 * self.UNIT), int(self.UNIT), int(self.UNIT))

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

        self.draw_timer(timer_time)

        if self.model.get_play_duplicate_sound():
            self.model.set_play_duplicate_sound(False)
            DUPLICATE_SOUND.play()

        if self.model.get_play_reveal_sound():
            self.model.set_play_reveal_sound(False)
            REVEAL_SOUND.play()

        if self.model.get_play_points_sound():
            self.model.set_play_points_sound(False)
            POINTS_SOUND.play()

        if self.model.get_play_no_points_sound():
            self.model.set_play_no_points_sound(False)
            NO_POINTS_SOUND.play()

        answer_grid = LocalRect(self.surface.get_rect()).resize(83 * self.UNIT, 39 * self.UNIT).move(0, 1 * self.UNIT)
        total_score = 0
        index = 0
        for column in answer_grid.columns(2):
            for cell in column.rows(5):
                answer_rect, score_rect = cell.inflate(-self.UNIT, 0).split_h(-8*self.UNIT)

                self.draw_shadow_box(answer_rect.inflate(int(-self.UNIT / 2), int(-self.UNIT / 2)))
                if self.model.get_answer(index) is not None:
                    self.draw_text(self.model.get_answer(index).upper(), answer_rect.inflate(int(-self.UNIT), int(-self.UNIT)))

                self.draw_shadow_box(score_rect.inflate(int(-self.UNIT / 2), int(-self.UNIT / 2)))
                if self.model.get_score(index) is not None:
                    self.draw_text(str(self.model.get_score(index)), score_rect.inflate(int(-self.UNIT), int(-self.UNIT)))
                    total_score += self.model.get_score(index)

                index += 1

        grand_total_rect = LocalRect(self.surface.get_rect()).resize(62 * self.UNIT, 8 * self.UNIT).move(0, 26 * self.UNIT)
        gt_label_rect, gt_score_rect = grand_total_rect.split_h(-11*self.UNIT)

        self.draw_shadow_box(gt_label_rect.inflate(int(-self.UNIT / 2), int(-self.UNIT / 2)))
        self.draw_text("GRAND TOTAL", gt_label_rect.inflate(int(-self.UNIT), int(-self.UNIT)))

        self.draw_shadow_box(gt_score_rect.inflate(int(-self.UNIT / 2), int(-self.UNIT / 2)))
        self.draw_text(str(total_score), gt_score_rect.inflate(int(-self.UNIT), int(-self.UNIT)))

