import math
import numpy as np

class Environment():
    def __init__(self, DIM, dt):
        self.DIM = DIM
        self.dt = dt
        self.particles = []

    def update(self):
        for this in self.particles:
            this.tick()



class Particle:
    def __init__(self, env, R, V, radius, color):
        self.env = env
        self.R = R
        self.V = V
        self.radius = radius
        self.color = color


    def move(self, r):
        self.R += r

    def tick(self):
        self.X += self.V*self.env.dt

    def timeToHit(self, that):
        if that is self:
            return math.inf
        dr = that.R - self.R
        dv = that.V - self.V
        dvdr = np.dot(dr, dv)

        if dvdr > 0:
            return math.inf

        dvdv = np.dot(dv,dv)
        drdr = np.dot(dr,dr)

        sigma = self.radius + that.radius

        d = dvdr**2 - dvdv*(drdr - sigma**2)

        if d < 0:
            return math.inf

        return -(dvdr + math.sqrt(d)) / dvdv

    def timeToHitVerticalWall(self):
        if self.R[0] > 0:
            return (1 - self.R[0] - self.radius) / self.V[0]
        elif self.R[0] < 0:
            return (self.radius - self.R[0]) / self.V[0]
        else:
            return math.inf

    def timeToHitHorizontalWall(self):
        if self.R[1] > 0:
            return (1 - self.R[1] - self.radius) / self.V[1]
        elif self.R[1] < 0:
            return (self.radius - self.R[1]) / self.V[1]
        else:
            return math.inf


    def bounceOff(self, that):
        mass = 0.05
        dr = that.R - self.R
        dv = that.V - self.V
        dvdr = np.dot(dr, dv)
        dist = self.radius + that.radius

        J = 2*mass*mass*dvdr / (mass*2 * dist)

        Jr = (J/dist)*dr

        self.r += Jr/mass

    def bounceOffVerticalWall():
        pass

    def bounceOffHorizontalWall():
        pass
