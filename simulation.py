import numpy as np
from options import *
from collection import Collection
import pandas as pd

class Simulation:
    def __init__(self, basis, canvas):
        self.t = 0
        self.q = []
        self.next = None
        self.canvas = canvas
        self.basis = basis
        self.stats = {
            "S":0,
            "I":0,
            "R":0
        }
        self.data = np.zeros((TOTAL_TICKS,4))
        self.data = pd.DataFrame(data=self.data, columns=["x", "S", "I", "R"])

    def infect(self):
        self.stats["S"] -= 1
        self.stats["I"] += 1

    def recover(self):
        self.stats["I"] -= 1
        self.stats["R"] += 1

    def cancel(self):
        self.canvas.after_cancel(self._job)

    def simulate(self, n, np, mobility, collections):
        parameters = {
            'n': n,
            'n0': np,
            'mobility': mobility
        }
        if collections == 4:
            self.collections = [Collection(self, parameters, [0, 0.5, 0, 0.5]),
                                Collection(self, parameters, [0, 0.5, 0.5, 1]),
                                Collection(self, parameters, [0.5, 1, 0, 0.5]),
                                Collection(self, parameters, [0.5, 1, 0.5, 1])]

        elif collections == 2:
            self.collections = [Collection(self, parameters, [0, 0.5, 0, 1]), Collection(self, parameters, [0.5, 1, 0, 1])]

        else:
            self.collections = [Collection(self, parameters)]


        self.collections_count = len(self.collections)
        self.loop()

    def loop(self):
        # print(self.t)
        # if self.t > TOTAL_TICKS:
        #     print("Stopp")
        #     self.cancel()
        #     self.basis.stop_simulation()

        self.canvas.delete('all')

        # Do everything inside collections
        for collection in self.collections:
            collection.doColisions()
            collection.step()
            if self.collections_count > 1:
                collection.draw_boundaries()


        self.t += 1

        self.data = self.data.append({
                                      'x': self.t,
                                      'S': self.stats['S'],
                                      'I': self.stats['I'],
                                      'R': self.stats['R']}, ignore_index=True)
        self._job = self.canvas.after(int(1000/FRAMES_PER_SECOND), self.loop)
