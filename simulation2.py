import numpy as np
import pygame
from pygame.locals import *
import time

from options import *

from queue import Queue

COLORS = {'B': (255, 255, 255),
          'S': (158, 237, 255),
          'I': (255, 196, 184),
          'R': (145, 255, 215)
          }

class Simulation:
    def __init__(self, xmax, ymax, fps, windowSurface, colors):
        self.xmax = xmax
        self.ymax = ymax
        self.FPS = fps
        self.windowSurface = windowSurface
        self.colors = colors
        self.t = 0
        self.q = []
        self.next = None

    def detectCollision(self, p, q):
        # Find the distance between two particles
        # dist = np.linalg.norm(p.r - q.r)
        dx = p.r[0] - q.r[0]
        dy = p.r[1] - q.r[1]
        dist = np.sqrt(dx**2 + dy**2)
        # sum_radius = p.radius*2
        sum_radius = RADIUS*2

        if dist < sum_radius:
            return True
        else:
            return False

    def changeDirection(self, dr):
        theta = np.arctan2(dr[1], dr[0])

        return np.array((np.cos(theta), np.sin(theta)))

    def collide(self, p, q):
        x = lambda a, b : a.v - (np.dot(a.v-b.v, a.r-b.r)/(np.linalg.norm(a.r - b.r)**2))*(a.r-b.r)

        p.v = x(p, q)
        q.v = x(q, p)
        # ar = self.changeDirection(q.r - p.r)
        # p.v -= ar
        # q.v = ar

        if p.status is "S" and q.status is "I":
            self.infect(p)
        elif q.status is "S" and p.status is "I":
            self.infect(q)

    def infect(self, particle):
        particle.status = "I"
        # Adds particle to queue with time + 5 sec
        self.q.append((self.t + TIME_TO_RECOVER, particle))

    def recover(self, particle):
        particle.status = "R"
        particle.hasMovement = False

    def addParticles(self, count):
        particles = []
        for i in range(count):
            hasMovement = False if np.random.uniform(100) < STATIC_PEOPLE_PERCENTAGE else True
            p = Particle(np.random.rand(2),
                         (2*np.random.rand(2)-1) * SPEED,
                         self.colors['susceptible'],
                         hasMovement)
            particles.append(p)
        self.particles = particles






    def display(self):
        for particle in self.particles:
            pygame.draw.circle(self.windowSurface, COLORS[particle.status], \
                                       (int(self.xmax * particle.r[0]), int(self.ymax * particle.r[1])), int(self.xmax*RADIUS), 0)
    def simulate(self):
        self.addParticles(NUMBER_OF_PEOPLE)

        self.infect(self.particles[3])

        pygame.display.set_caption('Covid-19 hermir')
        fpsClock = pygame.time.Clock()
        while self.t < TOTAL_TICKS:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    gameLoop = False

            self.windowSurface.fill(self.colors['background'])
            # Update positions
            [particle.step() for particle in self.particles]

            order = np.random.permutation(NUMBER_OF_PEOPLE)
            # Do collisions
            for i in range(len(self.particles)):
                for j in range(i + 1, len(self.particles)):
                    if self.detectCollision(self.particles[order[i]], \
                                            self.particles[order[j]]):
                        self.collide(self.particles[order[i]], \
                                     self.particles[order[j]])
                        break

            self.display()

            pygame.display.update()
            fpsClock.tick(self.FPS)
            self.t += 1

            for event in self.q:
                if event[0] == self.t:
                    self.recover(event[1])



# Takes in r=np.array((x,y)), v.np.array((vx,vy))
class Particle:
    def __init__(self, r, v, color, hasMovement = True):
        self.r = r
        self.v = v
        self.status = "S"
        self.hasMovement = hasMovement

    def step(self):
        if not self.hasMovement:
            return

        # Collide with walls
        if self.r[0] < 0 or self.r[0] > 1 :
           self.v[0] = -self.v[0]
        if self.r[1] < 0 or self.r[1] > 1 :
           self.v[1] = -self.v[1]

        self.r += self.v
