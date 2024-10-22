import pygame


class RectBuilder:
    def __init__(self, surface, rect=pygame.Rect(0, 0, 0, 0)):
        self.width = rect.width
        self.height = rect.height
        self.left = (surface.get_width() - self.width) / 2
        self.top = (surface.get_height() - self.height) / 2
        self.unit = min(surface.get_width() / 100, surface.get_height() / 75)

    def size(self, width, height):
        self.top += self.height / 2
        self.left += self.width / 2
        self.width = width * self.unit
        self.height = height * self.unit
        self.top -= self.height / 2
        self.left -= self.width / 2
        return self

    def done(self):
        return int(self.left), int(self.top), int(self.width), int(self.height)

    def translate(self, tx, ty):
        self.left += tx * self.unit
        self.top += ty * self.unit
        return self

    def unscaled_translate(self, tx, ty):
        self.left += tx
        self.top += ty
        return self
