import numpy as np
from options import *
from scipy import stats

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
        # Create array of length n with all values True
        self.has_movement = np.ones(parameters['n'], dtype=bool)
        self.recovery_time = np.full(parameters['n'], -1)
        self.contagiousness = np.full(parameters['n'], 20)
        self.rt = np.zeros(parameters['n'])
        self.time_to_infect = np.full(parameters['n'], -1)

        # Keep track of particle blinking
        # First element is index of blinking particle
        # Second is absolute time when blinking stops
        # Third is the state of the blink (yellow or normal)
        self.blinking = [-1, 0, 0]

        self.simulation = simulation
        self.simulation.stats['S'] += parameters['n']

        # Infect particles
        for i in np.random.randint(parameters['n'], size=parameters['n0']):
            self.infect(i)

        # Create super-spreaders
        for i in np.random.rand(3):
            self.contagiousness[int(i * parameters['n0'])] = 100

        for i in range(len(self.has_movement)):
            self.has_movement[i] = False if np.random.uniform(100) < parameters['mobility'] else True

    # Do collision on all particles in collection
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

    #Collide particles with indexes a and b
    def collide(self, a, b):
        x = lambda ar, av, br, bv : av - (np.dot(av-bv, ar-br)/(np.linalg.norm(ar - br)**2))*(ar-br)

        self.v[a, :] = x(self.r[a, :], self.v[a, :], self.r[b, :], self.v[b, :])
        self.v[b, :] = x(self.r[b, :], self.v[b, :], self.r[a, :], self.v[a, :])

        # Infect
        if self.status[a] == "S" and self.status[b] == "I":
            if self.contagiousness[b] > np.random.uniform(100) and self.simulation.t > self.time_to_infect[b]:
                self.rt[b] += 1
                self.infect(a)
        elif self.status[b] == "S" and self.status[a] == "I":
            if self.contagiousness[a] > np.random.uniform(100) and self.simulation.t > self.time_to_infect[a]:
                self.rt[a] += 1
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

        # Switch blinking state
        self.blinking[2] = 0 if self.blinking[2] == 1 else 1

    def infect(self, index):
        self.status[index] = "I"
        X = stats.beta(2, 5)  # Beta random variable 
        self.recovery_time[index] = int(self.simulation.t + X.rvs()*TIME_TO_RECOVER)
        self.time_to_infect[index] = int(self.simulation.t + X.rvs()*TIME_TO_INFECT)
        self.simulation.infect()

    def recover(self, index):
        self.status[index] = "R"
        self.simulation.recover()

    # Return color dynamically
    def color(self, index):
        # Handle blinking
        if self.blinking[0] == index and self.blinking[1] > self.simulation.t and self.blinking[2] == 1:
            return COLORS['B']

        # Normal colors
        if self.status[index] == "S":
            return COLORS['S']
        elif self.status[index] == 'R':
            return COLORS['R']
        elif self.status[index] == 'I':
            if self.contagiousness[index] > 70:  # Super-spreader
                return "#300101"
            else:
                return COLORS['I']

    def draw(self, index):
        self.simulation.canvas.create_oval(self.r[index, 0] * DIMENSIONS['width'] - RADIUS,
                                           self.r[index, 1] * DIMENSIONS['height'] - RADIUS,
                                           self.r[index, 0] * DIMENSIONS['width'] + RADIUS,
                                           self.r[index, 1] * DIMENSIONS['height'] + RADIUS,
                                           fill=self.color(index))

    def draw_boundaries(self, dash=None):

        # Coordinates of the four lines for each collection
        lines = [[0,2,0,3],[1,2,1,3],[0,2,1,2],[0,3,1,3]]

        for line in lines:
            self.simulation.canvas.create_line(self.boundaries[line[0]] * DIMENSIONS['width'],
                                               self.boundaries[line[1]] * DIMENSIONS['height'],
                                               self.boundaries[line[2]] * DIMENSIONS['width'],
                                               self.boundaries[line[3]] * DIMENSIONS['height'], dash=dash)

    # Takes in all neccesary data from particle and appends to current vectors
    def receive_particle(self,
                         status,
                         has_movement,
                         contagiousness,
                         recovery_time,
                         rt,
                         time_to_infect):
        # Create random position and velocity vectors
        r = np.random.rand(1, 2)
        v = 2 * (np.random.rand(1, 2) - 1) * SPEED
        r[:, 0] = (r[:, 0] * (self.boundaries[1] - self.boundaries[0])) + self.boundaries[0]
        r[:, 1] = (r[:, 1] * (self.boundaries[3] - self.boundaries[2])) + self.boundaries[2]

        self.r = np.append(self.r, r, axis=0)
        self.v = np.append(self.v, v, axis=0)
        self.status = np.append(self.status, status)
        self.has_movement = np.append(self.has_movement, has_movement)
        self.contagiousness = np.append(self.contagiousness, contagiousness)
        self.recovery_time = np.append(self.recovery_time, recovery_time)
        self.time_to_infect = np.append(self.time_to_infect, time_to_infect)
        self.rt = np.append(self.rt, rt)

        # Make new particle blink
        self.blinking = [len(self.rt)-1, self.simulation.t + 200, 1]

    # Remove particle i and return all its data
    def remove_particle(self, i):
        status = self.status[i]
        has_movement = self.has_movement[i]
        contagiousness = self.contagiousness[i]
        recovery_time = self.recovery_time[i]
        time_to_infect = self.time_to_infect[i]
        rt = self.rt[i]

        self.r = np.delete(self.r, i, axis=0)
        self.v = np.delete(self.v, i, axis=0)
        self.status = np.delete(self.status, i, axis=0)
        self.has_movement = np.delete(self.has_movement, i, axis=0)
        self.contagiousness = np.delete(self.contagiousness, i, axis=0)
        self.recovery_time = np.delete(self.recovery_time, i, axis=0)
        self.time_to_infect = np.delete(self.time_to_infect, i, axis=0)
        self.rt = np.delete(self.rt, i, axis=0)

        return status, has_movement, contagiousness, recovery_time, rt, time_to_infect

    # Get all rt data from infected or recovered praticles
    def get_rt(self):
        infected = np.argwhere(self.status[:] == "I")
        recovered = np.argwhere(self.status[:] == "R")
        return np.append(self.rt[infected], self.rt[recovered])
