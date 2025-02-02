# Simple pygame program
import os

# Import and initialize the pygame library
import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()

from scoreboard_model import ScoreboardModel
from scoreboard_view import ScoreboardView
from core.rpc import RPCServer
from threading import Thread

server = RPCServer()
model = ScoreboardModel()
server.registerInstance(model)
server_thread = Thread(target = server.run, daemon=True)
server_thread.start()

FULLSCREEN = True
if len(pygame.display.get_desktop_sizes()) == 1:
    FULLSCREEN = False


# Set up the drawing window
if FULLSCREEN:
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    infoObject = pygame.display.Info()
    SCREEN = pygame.display.set_mode((0, 0), pygame.NOFRAME, display=1)
    size_x = infoObject.current_w
    size_y = infoObject.current_h
else:
    size_x = 1920
    size_y = 1080
    SCREEN = pygame.display.set_mode([size_x, size_y])

# Run until the user asks to quit
running = True

view = ScoreboardView(model, SCREEN)

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    view.draw()

    # Flip the display
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()
