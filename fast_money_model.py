class FastMoneyModel:
    def __init__(self):
        self.timer_duration = 20
        self.timer_end_time = None
        self.timer_start = False
        self.play_duplicate_sound = False
        self.answer = [None] * 10
        self.score = [None] * 10

    def get_timer_duration(self):
        return self.timer_duration

    def set_timer_duration(self, timer_time):
        self.timer_duration = timer_time

    def get_timer_end_time(self):
        return self.timer_end_time

    def set_timer_end_time(self, timer_end_time):
        self.timer_end_time = timer_end_time

    def get_timer_start(self):
        return self.timer_start

    def set_timer_start(self, timer_start):
        self.timer_start = timer_start

    def get_play_duplicate_sound(self):
        return self.play_duplicate_sound

    def set_play_duplicate_sound(self, play_duplicate_sound):
        self.play_duplicate_sound = play_duplicate_sound

    def set_answer(self, index, answer):
        self.answer[index] = answer

    def get_answer(self, index):
        return self.answer[index]

    def set_score(self, index, score):
        self.score[index] = score

    def get_score(self, index):
        return self.score[index]
