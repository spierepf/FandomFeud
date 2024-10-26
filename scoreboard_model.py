from functools import wraps
from threading import Lock


def synchronized(member):
    @wraps(member)
    def wrapper(*args, **kwargs):
        lock = vars(member).get("_synchronized_lock", None)
        if lock is None:
            lock = vars(member).setdefault("_synchronized_lock", Lock())
        with lock:
            return member(*args, **kwargs)

    return wrapper


class ScoreboardModel:
    def __init__(self):
        self._scores = [0, 0]
        self._pot = 0
        self._newly_revealed = False
        self._revealed = []
        self._answers = []
        self._strike = None
        self._strike_start_time = None

    @synchronized
    def get_score(self, side):
        return self._scores[side.value]

    @synchronized
    def set_score(self, side, score):
        self._scores[side] = score

    @synchronized
    def get_pot(self):
        return self._pot

    @synchronized
    def set_pot(self, score):
        self._pot = score

    @synchronized
    def get_answer_count(self):
        return len(self._revealed)

    @synchronized
    def is_revealed_answer(self, i):
        return self._revealed[i]

    @synchronized
    def get_answer_text(self, i):
        return self._answers[i][0]

    @synchronized
    def get_answer_score(self, i):
        return self._answers[i][1]

    @synchronized
    def begin_round(self, answers):
        self._revealed = [False for _ in answers]
        self._answers = answers

    @synchronized
    def reveal_answer(self, i):
        self._newly_revealed |= not self._revealed[i]
        self._revealed[i] = True

    @synchronized
    def is_newly_revealed(self):
        return self._newly_revealed

    @synchronized
    def clear_newly_revealed(self):
        self._newly_revealed = False

    @synchronized
    def set_strike(self, strike):
        self._strike = strike

    @synchronized
    def get_strike(self):
        return self._strike

    @synchronized
    def set_strike_start_time(self, strike_start_time):
        self._strike_start_time = strike_start_time

    @synchronized
    def get_strike_start_time(self):
        return self._strike_start_time

    @synchronized
    def clear_strike(self):
        self._strike = None
        self._strike_start_time = None
