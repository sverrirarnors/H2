import math
import numpy as np
import queue as Q
import sys

import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
BLUE = (186, 247, 255)
RED = (255, 218, 212)

class Simulation():
    def __init__(self, DIM, dt, windowSurface):
        self.DIM = DIM
        self.dt = dt
        self.particles = []
        self.windowSurface = windowSurface
        self.t = 0




    def predict(self, a, limit):
        for particle in self.particles:
            print(a)
            dt = a.timeToHit(particle)
            if self.t + dt <= limit:
                self.pq.put(Event(self.t + dt, a, particle))

        dtX = a.timeToHitVerticalWall()
        dtY = a.timeToHitHorizontalWall()

        if self.t + dtX <= limit:
            self.pq.put(Event(self.t + dtX, a, None))
        if self.t + dtY <= limit:
            self.pq.put(Event(self.t + dtY, None, a))

    def redraw(self, limit):
        self.windowSurface.fill(WHITE)

        for particle in self.particles:
            pygame.draw.circle(self.windowSurface, particle.color,
                               (int(self.DIM[0] * particle.R[0,0]),
                                int(self.DIM[1] * particle.R[0,1])), int(particle.radius*self.DIM[0,0]/self.DIM[0,1]), 0)

    def simulate(self, limit):
        print(self.particles)
        self.pq = Q.PriorityQueue()
        for particle in self.particles:
            self.predict(particle, limit)

        self.pq.put(Event(0, None, None))

        while not self.pq.empty():
            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            e = self.pq.get()

            if not e.isValid():
                continue

            a = e.a
            b = e.b

            for particle in self.particles:
                particle.move(e.time - self.t)
            self.t = e.time

            if (a is not None and b is not None):
                a.bounceOff(b)
            elif (a is not None and b is None):
                a.bounceOffVerticalWall()
            elif (a is None and b is not None):
                b.bounceOffHorizontalWall
            elif (a is None and b is None):
                self.redraw(limit)

            self.predict(a, limit)
            self.predict(b, limit)

class Event:
    def __init__(self, t, a, b):
        self.time = t
        self.a = a
        self.b = b
        self.countA = a.count if a is not None else -1
        self.countB = b.count if b is not None else -1

    def __cmp__(self, other):
        return self.time - other.time

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time

    def isValid(self):
        if (self.a is not None and self.a.count != self.countA):
            return False

        if (self.b is not None and self.b.count != self.countB):
            return False

        return True


class Particle:
    def __init__(self, env, R, V, radius, color):
        self.env = env
        self.R = R
        self.V = V
        self.radius = radius
        self.color = color
        self.count = 0


    def move(self, r):
        self.R += r

    def tick(self):
        self.X += self.V*self.env.dt

    def timeToHit(self, that):
        if that is self:
            return math.inf
        dr = that.R - self.R
        dv = that.V - self.V
        dvdr = dr*dv

        if dvdr.any() > 0:
            return math.inf

        dvdv = dv*dv
        drdr = dr*dr

        sigma = self.radius + that.radius

        d = dvdr**2 - dvdv*(drdr - sigma**2)

        if d < 0:
            return math.inf

        return -(dvdr + math.sqrt(d)) / dvdv

    def timeToHitVerticalWall(self):
        if self.R[0,0] > 0:
            return (1 - self.R[0,0] - self.radius) / self.V[0,0]
        elif self.R[0,0] < 0:
            return (self.radius - self.R[0,0]) / self.V[0,0]
        else:
            return math.inf

    def timeToHitHorizontalWall(self):
        if self.R[0,1] > 0:
            return (1 - self.R[0,1] - self.radius) / self.V[0,1]
        elif self.R[0,1] < 0:
            return (self.radius - self.R[0,1]) / self.V[0,1]
        else:
            return math.inf

# https://algs4.cs.princeton.edu/code/edu/princeton/cs/algs4/Particle.java.html
# https://algs4.cs.princeton.edu/code/edu/princeton/cs/algs4/CollisionSystem.java.html
    def bounceOff(self, that):
        mass = 0.05
        dr = that.R - self.R
        dv = that.V - self.V
        dvdr = dr*dv
        dist = self.radius + that.radius

        J = 2*mass*mass*dvdr / (mass*2 * dist)

        Jr = (J/dist)*dr

        self.R += Jr/mass

        self.count += 1
        that.count += 1

    def bounceOffVerticalWall(self):
        self.R[0,0] *= -1
        self.count += 1

    def bounceOffHorizontalWall(self):
        self.R[0,1] *= -1
        self.count += 1

    def __str__(self):
        return f'({self.R[0,0]}, {self.R[0,1]})'
        # return str('Siggi')
