import numpy as np
from options import *

from particle import Particle
from options import *

COLORS = {'S': '#9eedff',
          'I': '#ffc4b8',
          'R': '#91ffd7'
          }

class Simulation:
    def __init__(self, canvas):
        self.t = 0
        self.q = []
        self.next = None
        self.canvas = canvas


    def detectCollision(self, p, q):
        # Find the distance between two particles
        # dist = np.linalg.norm(p.r - q.r)
        dx = (p.r[0] - q.r[0])*DIMENSIONS['width']
        dy = (p.r[1] - q.r[1])*DIMENSIONS['height']
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
        # p.v = -p.v
        # q.v = -q.v

        if p.status == "S" and q.status == "I":
            self.infect(p)
        elif q.status == "S" and p.status == "I":
            self.infect(q)

    def infect(self, particle):
        particle.status = "I"
        # Adds particle to queue with time + 5 sec
        self.q.append((self.t + TIME_TO_RECOVER, particle))
        particle.v *= 2

    def recover(self, particle):
        particle.status = "R"

    def addParticles(self, count):
        particles = []
        for i in range(count):
            hasMovement = False if np.random.uniform(100) < STATIC_PEOPLE_PERCENTAGE else True
            p = Particle(np.random.rand(2),
                         (2*np.random.rand(2)-1) * SPEED,
                         COLORS['S'],
                         self.canvas,
                         hasMovement)
            particles.append(p)
        self.particles = particles

    def cancel(self):
        self.canvas.after_cancel(self._job)

    def simulate(self, n, np):
        self.n = n
        # self.addParticles(NUMBER_OF_PEOPLE)
        self.addParticles(n)

        for i in range(np):
            self.infect(self.particles[i])


        self.loop()

    def loop(self):
        self.canvas.delete('all')
        # Update positions
        [particle.step() for particle in self.particles]

        order = np.random.permutation(self.n)
        # Do collisions
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                if self.detectCollision(self.particles[order[i]], \
                                        self.particles[order[j]]):
                    self.collide(self.particles[order[i]], \
                                 self.particles[order[j]])
                    break


        self.t += 1
        for event in self.q:
            if event[0] == self.t:
                self.recover(event[1])

        self._job = self.canvas.after(int(1000/FRAMES_PER_SECOND), self.loop)
