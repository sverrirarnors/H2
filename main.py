import numpy as np
import tkinter as tk
from tkinter import font  as tkfont

from options import *
from simulation import Simulation

# For plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd


class Basis(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, columnspan=4)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.label = tk.Label(self, text="COVID-19 hermir", font = tkfont.Font(family='Helvetica', size=18, weight="bold"))
        self.canvas = tk.Canvas(self,
                           width=DIMENSIONS['width'],
                           height=DIMENSIONS['height'], borderwidth=2, relief='solid')

        self.label.grid(row=1, columnspan=4)
        self.canvas.grid(row=2, columnspan=4)
        self.canvas.config(bg="white")


        # Population-slider
        self.pop_label = tk.Label(self, text="Fólksfjöldi", font = tkfont.Font(family='Helvetica', size=18, weight="normal"))
        self.pop_label.grid(row=3, columnspan=2)
        self.pop = tk.Scale(self, from_=50, to=150, orient="horizontal")
        self.pop.grid(row=4, columnspan=2)

        # Number of infected
        self.n0_label = tk.Label(self, text="Fjöldi smitaðra", font = tkfont.Font(family='Helvetica', size=18, weight="normal"))
        self.n0 = tk.Scale(self, from_=1, to=10, orient="horizontal")
        self.n0_label.grid(row=3, column=2)
        self.n0.grid(row=4, column=2)

        # Mobility
        self.mobility_label = tk.Label(self, text="Hreyfanleiki (samkomubann)", font = tkfont.Font(family='Helvetica', size=18, weight="normal"))
        self.mobility = tk.Scale(self, from_=0, to=100, orient="horizontal")
        self.mobility_label.grid(row=3, column=3)
        self.mobility.grid(row=4, column=3)

        # Start and stop
        self.begin = tk.Button(self, text="Byrja", command= self.start_simulation)
        self.begin.grid(row=5, columnspan=2)
        self.stop = tk.Button(self, text="Hætta", command=self.stop_simulation)
        self.stop.configure(state='disabled')
        self.stop.grid(row=5, column = 1, columnspan=2)

        # Graph
        x = np.arange(0, 2*np.pi, 0.01)
        self.fig = plt.Figure()
        self.plot = self.fig.add_subplot(111)
        self.graph = FigureCanvasTkAgg(self.fig, master=self)
        self.graph.get_tk_widget().grid(column=8, columnspan=2, rowspan=1, row=2)
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=100)


    def start_simulation(self):
        self.begin.configure(state='disabled')
        self.pop.configure(state='disabled')
        self.stop.configure(state='normal')
        self.s = Simulation(self, self.canvas)
        self.s.simulate(self.pop.get(), self.n0.get(), self.mobility.get())

    def stop_simulation(self):
        self.begin.configure(state='normal')
        self.pop.configure(state='normal')
        self.stop.configure(state='disabled')
        self.s.cancel()
        self.canvas.delete('all')

    def animate(self, i):
        print("Keyrir")
        data = pd.read_csv('gogn.csv')
        x = data['x']
        susceptible = data['S']
        infected = data['I']
        removed = data['R']
        # x = s.t
        # susceptible = s.stats["S"]
        # infected = s.stats["I"]
        # removed = s.stats["R"]

        self.plot.cla()

        self.plot.plot(x, susceptible, label='S')
        self.plot.plot(x, infected, label='I')
        self.plot.plot(x, removed, label='R')


if __name__ == "__main__":
    app = Basis()
    app.title("COVID-19 hermun")
    app.resizable(False, False)
    app.mainloop()
