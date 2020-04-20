import numpy as np
from options import *
from collection import Collection
import pandas as pd

class Simulation:
    def __init__(self, basis, canvas):
        self.t = 0
        self.q = []
        self.canvas = canvas
        self.basis = basis
        self.stats = {
            "S":0,
            "I":0,
            "R":0
        }

        # Initialize dataframe for stats
        self.data = np.zeros((1,4))
        self.data = pd.DataFrame(data=self.data, columns=["x", "S", "I", "R"])
        self.average_rt = 0

    def infect(self):
        self.stats["S"] -= 1
        self.stats["I"] += 1

    def recover(self):
        self.stats["I"] -= 1
        self.stats["R"] += 1

    def stop(self):
        self.stop_simulation = True

    # Takes in total population, total number of infected, and number of collections
    def simulate(self, n, np, mobility, collections, do_collisions):
        parameters = {
            'n': n,
            'n0': np,
            'mobility': mobility,
            'do_collisions': do_collisions
        }
        self.collections = []

        # Different cases for number of collections
        # Coordinates is an array of relative coordinates on the form [x1, x2, y1, y2]
        # Ratio is the ratio of the population each collection gets (based on Iceland's population)
        if collections == 4:
            coordinates = [[0, 0.5, 0, 0.5], [0, 0.5, 0.5, 1], [0.5, 1, 0, 0.5], [0.5, 1, 0.5, 1]]
            ratios = [0.152, 0.705, 0.037, 0.106]
            for coordinate, ratio in zip(coordinates, ratios):
                self.collections.append(Collection(self,
                                                   {'n': int(n * ratio), 'n0': int(np * ratio), 'mobility': mobility, 'do_collisions': do_collisions},
                                                   coordinate))

        elif collections == 2:
            coordinates = [[0, 0.5, 0, 1], [0.5, 1, 0, 1]]
            ratios = [0.64, 0.36]
            for coordinate, ratio in zip(coordinates, ratios):
                self.collections.append(Collection(self,
                                                   {'n': int(n * ratio), 'n0': int(np * ratio), 'mobility': mobility, 'elastic': do_collisions},
                                                   coordinate))

        else:
            self.collections = [Collection(self, parameters)]

        self.collections_count = len(self.collections)
        self.stop_simulation = False
        self.loop()

    def loop(self):
        # Check if we have to stop the simulation, stops if no particles are infected
        if (MIN_TIME < self.t < MAX_TIME and self.data["I"].iloc[-1] < 1) or self.stop_simulation is True:
            self.canvas.after_cancel(_job)
            self.basis.stop_simulation()

        self.canvas.delete('all')
        # Keep track of rt values for particles
        self.rt = np.zeros([])
        # Do everything inside collections
        for collection in self.collections:
            collection.doColisions()
            collection.step()
            # Get all rt values from collection
            self.rt = np.append(self.rt, collection.get_rt())

            if self.collections_count > 1:
                # Teleportation logic
                i = np.random.randint(0, len(self.collections))
                population_limit = 3
                can_give = len(self.collections[i-1].r) > population_limit
                if TELEPORT_ODDS_PERCENTAGE > np.random.uniform(100) and can_give:
                    self.collections[i].receive_particle(*self.collections[i-1].remove_particle(0))
                # Draw lines for boundaries
                collection.draw_boundaries()


        self.average_rt = np.average(self.rt)
        self.t += 1

        self.data = self.data.append({
                                      'x': self.t,
                                      'S': self.stats['S'],
                                      'I': self.stats['I'],
                                      'R': self.stats['R']}, ignore_index=True)

        # Loop again after 1/FPS sec
        _job = self.canvas.after(int(1000/FRAMES_PER_SECOND), self.loop)
