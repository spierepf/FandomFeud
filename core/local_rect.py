import pygame


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
