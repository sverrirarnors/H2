import numpy as np
from options import *
import cProfile
cp = cProfile.Profile()

COLORS = {'S': '#9eedff',
          'I': '#ffc4b8',
          'R': '#91ffd7'
          }
class Collection:
    def __init__(self, simulation):
        n = 500
        self.r = np.random.rand(n, 2)
        self.v = (2 * np.random.rand(n, 2) - 1) * SPEED
        self.status = np.repeat('S', n)
        self.has_movement = np.ones(n, dtype=bool)
        self.recovery_time = np.full((n, 2), np.inf)
        self.simulation = simulation

        self.simulation.stats['S'] += n

        self.status[0] = "I"

        for i in range(len(self.has_movement)):
            self.has_movement[i] = False if np.random.uniform(100) < STATIC_PEOPLE_PERCENTAGE else True

    def doColisions(self):
        cp.enable()
        r = np.column_stack((
                             self.r[:, 0] * DIMENSIONS['width'],
                             self.r[:, 1] * DIMENSIONS['height']))
        # r = np.zeros((100, 2))
        # r[:, 0] = self.r[:, 0] * DIMENSIONS['width']
        # r[:, 1] = self.r[:, 1] * DIMENSIONS['height']
        for i in range(len(self.r)):
            distances = np.hypot(*(r - r[i, :]).T)
            to_resolve = np.argwhere(distances[:] < RADIUS)

            for j in to_resolve:
                if i != j[0]:
                    self.collide(i, j[0])
        cp.disable()
        cp.print_stats()


    def collide(self, a, b):
        x = lambda ar, av, br, bv : av - (np.dot(av-bv, ar-br)/(np.linalg.norm(ar - br)**2))*(ar-br)

        self.v[a, :] = x(self.r[a, :], self.v[a, :], self.r[b, :], self.v[b, :])
        self.v[b, :] = x(self.r[b, :], self.v[b, :], self.r[a, :], self.v[a, :])

        # Infect
        if self.status[a] == "S" and self.status[b] == "I":
            self.infect(a)
        elif self.status[a] == "S" and self.status[b] == "I":
            self.infect(b)

    def step(self):
        # Check for colission with walls
        left = np.argwhere(self.r[:, 0] < 0)
        self.v[left, 0] = self.v[left, 0] * -1

        right = np.argwhere(self.r[:, 0] > 1)
        self.v[right, 0] = self.v[right, 0] * -1

        top = np.argwhere(self.r[:, 1] > 1)
        self.v[top, 1] = self.v[top, 1] * -1

        bottom = np.argwhere(self.r[:, 1] < 0)
        self.v[bottom, 1] = self.v[bottom, 1] * -1

        self.r = self.r + self.v

        # Draw particles
        [self.draw(i) for i in range(len(self.r))]

        # Recover
        recovered = np.argwhere(self.recovery_time == self.simulation.t)
        [self.recover(i) for i in recovered]

    def infect(self, index):
        self.status[index] = "I"
        self.recovery_time[index] = self.simulation.t + TIME_TO_RECOVER
        self.simulation.infect()

    # Called from simulation class
    def recover(self, index):
        self.status[index] = "R"
        self.simulation.recover()

    def draw(self, index):
        self.simulation.canvas.create_oval(self.r[index, 0] * DIMENSIONS['width'] - RADIUS,
                                           self.r[index, 1] * DIMENSIONS['height'] - RADIUS,
                                           self.r[index, 0] * DIMENSIONS['width'] + RADIUS,
                                           self.r[index, 1] * DIMENSIONS['height'] + RADIUS,
                                           fill=COLORS[self.status[index]])
