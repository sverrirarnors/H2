import sys
import pygame
from pygame.locals import *

# set up the colors (RGB - red-green-blue values)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# set up pygame
pygame.init()

# set up the window. Upper left corner is (0,0)
xmax = 600
ymax = 400
windowSurface = pygame.display.set_mode((xmax, ymax))
pygame.display.set_caption('pyGame prufa')

FRAMES_PER_SECOND = 30
fpsClock = pygame.time.Clock()

# run the main loop
while True:
    # Clear screen
    windowSurface.fill(WHITE)

    # Draw components
    pygame.draw.circle(windowSurface, BLUE, (200, 300), 32)

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FRAMES_PER_SECOND)
