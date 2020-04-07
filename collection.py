import numpy as np
from options import *


class Collection:
    def __init__(self, simulation):
        self.r = np.random.rand(100, 2)
        self.v = (2 * np.random.rand(100, 22) - 1) * SPEED
        self.status = np.repeat('S', 100)
        self.has_movement = np.ones(100, dtype=bool)
        self.recovery_time = np.full((100, 2), np.inf)
        self.simulation = simulation

        for i in range(len(self.has_movement)):
            self.has_movement[i] = False if np.random.uniform(100) < STATIC_PEOPLE_PERCENTAGE else True

    def doColisions(self):
        r = np.column_stack((
                             self.r[:, 0] * DIMENSIONS['width'],
                             self.r[:, 1] * DIMENSIONS['height']))
        for i in range(len(self.r)):
            distances = np.hypot(*(r - r[i, :]).T)
            to_resolve = np.argwhere(distances[:] < RADIUS)

            for j in to_resolve:
                self.collide(i, j)

    def collide(self, a, b):
        x = lambda a, b : a - (np.dot(a-b, a-b)/(np.linalg.norm(a - b)**2))*(a-b)

        self.v[a, :] = x(self.v[a, :], self.v[b, :])
        self.v[b, :] = x(self.v[b, :], self.v[a, :])

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
        self.recovery_time = self.simulation.t + TIME_TO_RECOVER
        self.simulation.infect()

    # Called from simulation class
    def recover(self, index):
        self.status[index] = "R"
        self.simulation.recover()

    def draw(self, index):
        self.simulation.canvas.create_oval(self.r[0]*DIMENSIONS['width'] - RADIUS,
                                             self.r[1]*DIMENSIONS['height'] - RADIUS,
                                             self.r[0]*DIMENSIONS['width'] + RADIUS,
                                             self.r[1]*DIMENSIONS['height'] + RADIUS,
                                             fill=COLORS[self.status])
