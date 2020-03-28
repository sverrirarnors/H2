import sys
import numpy as np
import pygame
from pygame.locals import *

# set up the colors (RGB - red-green-blue values)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# set up pygame
pygame.init()

# set up the window
xmax = 600
ymax = 400
windowSurface = pygame.display.set_mode((xmax, ymax))
pygame.display.set_caption('Covid-19 hermir')

FRAMES_PER_SECOND = 30
fpsClock = pygame.time.Clock()

n = 50 # Number of points
frozen = 0.5 # Fraction of points that do not move
p_unfreeze = 0.01 # Probability of a frozen point going on the move
speed = 0.01
radius = 5

# Initial coordinates are uniformly random in (0, 1)
x = np.random.rand(n)
y = np.random.rand(n)

# Point velocity is uniformly random in (0, speed)
vx = speed * np.random.rand(n)
vy = speed * np.random.rand(n)
for i in range(int(frozen*n)):
    vx[i] = 0
    vy[i] = 0

# run the main loop
while True:
    # Clear screen
    windowSurface.fill(WHITE)

    # Update positions
    for i in range(n):
        # Reverse directon if point hits the boundary
        if x[i] < 0 or x[i] > 1:
            vx[i] = -1 * vx[i]
        if y[i] < 0 or y[i] > 1:
            vy[i] = -1 * vy[i]
        x[i] += vx[i]
        y[i] += vy[i]

        # Frozen points start moving with probability p_unfreeze
        if vx[i] == 0 and vy[i] == 0 and np.random.rand() < p_unfreeze:
            vx[i] = speed * np.random.rand()
            vy[i] = speed * np.random.rand()

    # Redraw
    for i in range(n):
        pygame.draw.circle(windowSurface, BLUE, \
                           (int(xmax * x[i]), int(ymax * y[i])), radius, 0)

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FRAMES_PER_SECOND)
