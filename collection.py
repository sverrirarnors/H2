import numpy as np
from options import *
from scipy import stats

COLORS = {'S': '#A3E0FF',
          'I': '#FFB0B7',
          'R': '#8AFFA5'
          }
# Boundaries on the form [x1, x2, y1, y2]
class Collection:
    def __init__(self, simulation, parameters, boundaries=[0, 1, 0, 1]):
        self.boundaries = boundaries
        self.r = np.random.rand(parameters['n'], 2)
        # Scale r vectors to right boundaries
        self.r = np.column_stack((
                                  (self.r[:, 0] * (self.boundaries[1] - self.boundaries[0])) + self.boundaries[0],
                                  (self.r[:, 1] * (self.boundaries[3] - self.boundaries[2])) + self.boundaries[2]
        ))
        self.v = (2 * np.random.rand(parameters['n'], 2) - 1) * SPEED
        self.status = np.repeat('S', parameters['n'])
        self.has_movement = np.ones(parameters['n'], dtype=bool)
        self.recovery_time = np.full(parameters['n'], -1)
        self.contagiousness = np.full(parameters['n'], 20)
        self.simulation = simulation
        self.simulation.stats['S'] += parameters['n']

        for i in range(parameters['n0']):
            self.infect(i)


        for i in np.random.rand(3):
            self.contagiousness[int(i * parameters['n0'])] = 100

        for i in range(len(self.has_movement)):
            self.has_movement[i] = False if np.random.uniform(100) < parameters['mobility'] else True

    def doColisions(self):
        r = np.column_stack((
                             self.r[:, 0] * DIMENSIONS['width'],
                             self.r[:, 1] * DIMENSIONS['height']))
        for i in range(len(self.r)):
            distances = np.hypot(*(r - r[i, :]).T)
            to_resolve = np.argwhere(distances[:] < RADIUS * 2)

            for j in to_resolve:
                if i != j[0]:
                    self.collide(i, j[0])


    def collide(self, a, b):
        x = lambda ar, av, br, bv : av - (np.dot(av-bv, ar-br)/(np.linalg.norm(ar - br)**2))*(ar-br)

        self.v[a, :] = x(self.r[a, :], self.v[a, :], self.r[b, :], self.v[b, :])
        self.v[b, :] = x(self.r[b, :], self.v[b, :], self.r[a, :], self.v[a, :])

        # Infect
        if self.status[a] == "S" and self.status[b] == "I":
            if self.contagiousness[b] > np.random.uniform(100):
                self.infect(a)
        elif self.status[a] == "S" and self.status[b] == "I":
            if self.contagiousness[a] > np.random.uniform(100):
                self.infect(b)

    def step(self):

        # Check for colission with walls
        left = np.argwhere(self.r[:, 0] < self.boundaries[0])
        self.v[left, 0] = self.v[left, 0] * -1

        right = np.argwhere(self.r[:, 0] > self.boundaries[1])
        self.v[right, 0] = self.v[right, 0] * -1

        top = np.argwhere(self.r[:, 1] < self.boundaries[3])
        self.v[top, 1] = self.v[top, 1] * -1

        bottom = np.argwhere(self.r[:, 1] > self.boundaries[2])
        self.v[bottom, 1] = self.v[bottom, 1] * -1

        to_move = self.has_movement[:] == True
        self.r[to_move] = self.r[to_move] + self.v[to_move]

        # Draw particles
        [self.draw(i) for i in range(len(self.r))]
        # Recover
        recovered = np.argwhere(self.recovery_time == self.simulation.t)
        [self.recover(i) for i in recovered]

    def infect(self, index):
        self.status[index] = "I"
        X = stats.beta(2,5) # Beta random variable 
        self.recovery_time[index] = int(self.simulation.t + X.rvs()*TIME_TO_RECOVER)
        self.simulation.infect()

    # Called from simulation class
    def recover(self, index):
        self.status[index] = "R"
        self.simulation.recover()

    def color(self, index):
        if self.status[index] == "S":
            return COLORS['S']
        elif self.status[index] == 'R':
            return COLORS['R']
        elif self.status[index] == 'I':
            if self.contagiousness[index] > 70:
                return "#300101"
            else:
                return COLORS['I']
    def draw(self, index):
        self.simulation.canvas.create_oval(self.r[index, 0] * DIMENSIONS['width'] - RADIUS,
                                           self.r[index, 1] * DIMENSIONS['height'] - RADIUS,
                                           self.r[index, 0] * DIMENSIONS['width'] + RADIUS,
                                           self.r[index, 1] * DIMENSIONS['height'] + RADIUS,
                                           fill=self.color(index))

    def draw_boundaries(self):
        self.simulation.canvas.create_line(self.boundaries[0] * DIMENSIONS['width'],
                                           self.boundaries[2] * DIMENSIONS['height'],
                                           self.boundaries[0] * DIMENSIONS['width'],
                                           self.boundaries[3] * DIMENSIONS['height'])

        self.simulation.canvas.create_line(self.boundaries[1] * DIMENSIONS['width'],
                                           self.boundaries[2] * DIMENSIONS['height'],
                                           self.boundaries[1] * DIMENSIONS['width'],
                                           self.boundaries[3] * DIMENSIONS['height'])

        self.simulation.canvas.create_line(self.boundaries[0] * DIMENSIONS['width'],
                                           self.boundaries[2] * DIMENSIONS['height'],
                                           self.boundaries[1] * DIMENSIONS['width'],
                                           self.boundaries[2] * DIMENSIONS['height'])

        self.simulation.canvas.create_line(self.boundaries[0] * DIMENSIONS['width'],
                                           self.boundaries[3] * DIMENSIONS['height'],
                                           self.boundaries[1] * DIMENSIONS['width'],
                                           self.boundaries[3] * DIMENSIONS['height'])
