import numpy as np
import pygame
from pygame.locals import *
import time

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

    def collide(self, p, q):
        x = lambda a, b : a.v - (np.dot(a.v-b.v, a.r-b.r)/(np.linalg.norm(a.r - b.r)**2))*(a.r-b.r)
        p.v = x(p, q)
        q.v = x(q, p)

        if p.status is "S" and q.status is "I":
            self.infect(p)
        elif q.status is "S" and p.status is "I":
            self.infect(q)

    def infect(self, particle):
        particle.status = "I"
        # Adds particle to queue with time + 5 sec
        self.q.append((self.t + 100, particle))

    def recover(self, particle):
        particle.status = "R"

    def addParticles(self, count):
        particles = []
        for i in range(count):
            p = Particle(np.random.rand(2),
                         np.random.rand(2)*0.01,
                         self.colors['susceptible'],
                         0.02)
            particles.append(p)
        self.particles = particles






    def display(self):
        for particle in self.particles:
            pygame.draw.circle(self.windowSurface, COLORS[particle.status], \
                                       (int(self.xmax * particle.r[0]), int(self.ymax * particle.r[1])), int(self.xmax*particle.radius), 0)
    def simulate(self):
        self.addParticles(10)

        self.infect(self.particles[3])

        pygame.display.set_caption('Covid-19 hermir')
        fpsClock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    gameLoop = False

            self.windowSurface.fill(self.colors['background'])
            # Update positions
            [particle.step() for particle in self.particles]


            # Do collisions
            for i in range(len(self.particles)):
                for j in range(i + 1, len(self.particles)):
                    if self.particles[i].detectCollision(self.particles[j]):
                        self.collide(self.particles[i], self.particles[j])
                        break
            # for a in self.particles:
            #     for b in self.particles:
            #         if a is not b and a.detectCollision(b):
            #             a.collide(b)
            #             break

            # Display particles
            self.display()

            pygame.display.update()
            fpsClock.tick(self.FPS)
            self.t += 1

            for event in self.q:
                if event[0] == self.t:
                    self.recover(event[1])



# Takes in r=np.array((x,y)), v.np.array((vx,vy))
class Particle:
    def __init__(self, r, v, color, radius):
        self.r = r
        self.v = v
        self.radius = radius
        self.status = "S"

    def detectCollision(self, other):
        # Find the distance between two particles
        dist = np.hypot(*(self.r - other.r))
        sum_radius = self.radius + other.radius

        if dist <= sum_radius:
            return True
        else:
            return False




    def step(self):
        # Collide with walls
       if self.r[0] < 0 or self.r[0] > 1 :
           self.v[0] = -self.v[0]
       if self.r[1] < 0 or self.r[1] > 1 :
           self.v[1] = -self.v[1]

       self.r += self.v
