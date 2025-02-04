import pygame


class PygameView:
    def __init__(self, model, surface):
        self.bg = pygame.image.load("FamilyFeud_PurpleBG.jpg")
        self.model = model
        self.surface = surface
        self.UNIT = min(surface.get_width() / 100, surface.get_height() / 75)

    def draw_background(self):
        for x in range(0, self.surface.get_width(), self.bg.get_width()-300):
            for y in range(0, self.surface.get_height(), self.bg.get_height()-127):
                self.surface.blit(self.bg, (x, y))

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
