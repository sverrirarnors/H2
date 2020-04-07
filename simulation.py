import numpy as np
from options import *
from collection import Collection
import pandas as pd

COLORS = {'S': '#9eedff',
          'I': '#ffc4b8',
          'R': '#91ffd7'
          }

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

    def simulate(self, n, np, mobility):
        self.n = n
        self.mobility = mobility
        # self.addParticles(NUMBER_OF_PEOPLE)

        self.collections = [Collection(self)]

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


        self.t += 1

        # self.stats[self.t, :] = np.array((self.t,
        #                                   self.stats['S'],
        #                                   self.stats['I'],
        #                                   self.stats['R']))
        self.data = self.data.append({
                                      'x': self.t,
                                      'S': self.stats['S'],
                                      'I': self.stats['I'],
                                      'R': self.stats['R']}, ignore_index=True)
        self._job = self.canvas.after(int(1000/FRAMES_PER_SECOND), self.loop)
