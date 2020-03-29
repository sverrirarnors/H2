import numpy as np
import pygame
from pygame.locals import *

class Simulation:
    def __init__(self, xmax, ymax, fps, windowSurface, colors):
        self.xmax = xmax
        self.ymax = ymax
        self.FPS = fps
        self.windowSurface = windowSurface
        self.colors = colors

    def addParticles(self, count):
        particles = []
        for i in range(count):
            p = Particle(np.random.rand(2),
                         np.random.rand(2)*0.01,
                         self.colors['susceptible'],
                         0.03)
            particles.append(p)
        self.particles = particles




    def display(self):
        for particle in self.particles:
            pygame.draw.circle(self.windowSurface, particle.color, \
                                       (int(self.xmax * particle.r[0]), int(self.ymax * particle.r[1])), int(self.xmax*particle.radius), 0)
    def simulate(self):
        self.addParticles(10)

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
            for a in self.particles:
                for b in self.particles:
                    print(a.detectCollision(b))
                    if a.detectCollision(b):
                        a.collide(b)
                        break

            # Display particles
            self.display()

            pygame.display.update()
            fpsClock.tick(self.FPS)

# Takes in r=np.array((x,y)), v.np.array((vx,vy))
class Particle:
    def __init__(self, r, v, color, radius):
        self.r = r
        self.v = v
        self.color = color
        self.radius = radius

    def detectCollision(self, other):
        # Find the distance between two particles
        dist = np.linalg.norm(self.r - other.r)
        sum_radius = self.radius + other.radius

        if dist <= sum_radius:
            return True
        else:
            return False

    def collide(self, other):
        print("skipti um staðsetningu")
        self.v = -1*self.v

        other.v = -1*other.v


    def step(self):
        # Collide with walls
       if self.r[0] < 0 or self.r[0] > 1 :
           self.v[0] = -self.v[0]
       if self.r[1] < 0 or self.r[1] > 1 :
           self.v[1] = -self.v[1]

       self.r += self.v
