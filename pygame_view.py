import pygame


class PygameView:
    def __init__(self, model, surface):
        self.bg = pygame.image.load("FamilyFeud_PurpleBG.jpg")
        self.model = model
        self.surface = surface
        self.UNIT = min(surface.get_width() / 100, surface.get_height() / 75)
        self.inner_border_width = 61
        self.inner_border_height = 38
        self.box_width = (self.inner_border_width - 2) / 2
        self.box_height = (self.inner_border_height - 2) / 4

    def draw_background(self):
        for x in range(0, self.surface.get_width(), self.bg.get_width()-300):
            for y in range(0, self.surface.get_height(), self.bg.get_height()-127):
                self.surface.blit(self.bg, (x, y))