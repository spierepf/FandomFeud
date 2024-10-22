# Simple pygame program

# Import and initialize the pygame library
import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()

from scoreboard_model import ScoreboardModel
from scoreboard_view import ScoreboardView
from rpc import RPCServer
from threading import Thread

server = RPCServer()
model = ScoreboardModel()
server.registerInstance(model)
server_thread = Thread(target = server.run, daemon=True)
server_thread.start()

FULLSCREEN = False

# Set up the drawing window
if FULLSCREEN:
    infoObject = pygame.display.Info()
    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    size_x = infoObject.current_w
    size_y = infoObject.current_h
else:
    size_x = 1024
    size_y = 768
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