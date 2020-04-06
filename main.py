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

COLORS = {'S': '#9eedff',
          'I': '#ffc4b8',
          'R': '#91ffd7'
          }

class Basis(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, columnspan=4)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.label = tk.Label(self.container, text="COVID-19 hermir", font = tkfont.Font(family='Helvetica', size=18, weight="bold"))
        self.canvas = tk.Canvas(self.container,
                           width=DIMENSIONS['width'],
                           height=DIMENSIONS['height'], borderwidth=2, relief='solid')

        self.label.grid(row=1, columnspan=4)
        self.canvas.grid(row=2, columnspan=4)
        self.canvas.config(bg="white")
        self.s = Simulation(self, self.canvas)


        # Population-slider
        self.pop_label = tk.Label(self.container, text="Fólksfjöldi", font = tkfont.Font(family='Helvetica', size=18, weight="normal"))
        self.pop_label.grid(row=3, columnspan=2)
        self.pop = tk.Scale(self.container, from_=50, to=150, orient="horizontal")
        self.pop.grid(row=4, columnspan=2)

        # Number of infected
        self.n0_label = tk.Label(self.container, text="Fjöldi smitaðra", font = tkfont.Font(family='Helvetica', size=18, weight="normal"))
        self.n0 = tk.Scale(self.container, from_=1, to=10, orient="horizontal")
        self.n0_label.grid(row=3, column=2)
        self.n0.grid(row=4, column=2)

        # Mobility
        self.mobility_label = tk.Label(self.container, text="Hreyfanleiki (samkomubann)", font = tkfont.Font(family='Helvetica', size=18, weight="normal"))
        self.mobility = tk.Scale(self.container, from_=0, to=100, orient="horizontal")
        self.mobility_label.grid(row=3, column=3)
        self.mobility.grid(row=4, column=3)

        # Start and stop
        self.begin = tk.Button(self.container, text="Byrja", command= self.start_simulation)
        self.begin.grid(row=5, columnspan=2)
        self.stop = tk.Button(self.container, text="Hætta", command=self.stop_simulation)
        self.stop.configure(state='disabled')
        self.stop.grid(row=5, column = 1, columnspan=2)

        # Graph
        # plt.style.use("ggplot")
        self.fig = plt.Figure()
        self.plot = self.fig.add_subplot(111)
        self.plot.axes.get_xaxis().set_visible(False)
        self.plot.axes.get_yaxis().set_visible(False)
        self.graph = FigureCanvasTkAgg(self.fig, master=self.container)
        self.graph.get_tk_widget().grid(column=8, columnspan=2, rowspan=1, row=2)
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=100)

        self.dashboard = tk.Frame(self.container, borderwidth = 1)
        self.dashboard.grid(row=2, rowspan=1, column=8)

        self.S_label_var = tk.StringVar(self.dashboard)
        self.S_label = tk.Label(self.dashboard, textvariable=self.S_label_var)
        self.S_label.grid(row=1)

        self.I_label_var = tk.StringVar(self.dashboard)
        self.I_label = tk.Label(self.dashboard, textvariable=self.I_label_var)
        self.I_label.grid(row=2)

        self.R_label_var = tk.StringVar(self.dashboard)
        self.R_label = tk.Label(self.dashboard, textvariable=self.R_label_var)
        self.R_label.grid(row=3)



    def start_simulation(self):
        self.begin.configure(state='disabled')
        self.pop.configure(state='disabled')
        self.n0.configure(state='disabled')
        self.mobility.configure(state='disabled')
        self.stop.configure(state='normal')
        self.s = Simulation(self, self.canvas)
        self.s.simulate(self.pop.get(), self.n0.get(), self.mobility.get())

    def stop_simulation(self):
        self.begin.configure(state='normal')
        self.pop.configure(state='normal')
        self.n0.configure(state='normal')
        self.mobility.configure(state='normal')
        self.stop.configure(state='disabled')
        self.s.cancel()
        self.canvas.delete('all')

    def animate(self, i):
        # data = pd.read_csv('gogn.csv')
        # x = self.s.data[0,:]
        # susceptible = self.s.data[1,:]
        # infected = self.s.data[2,:]
        # removed = self.s.data[3,:]

        # self.S_label_var.set(f'Heilbrigðir: {str(susceptible[len(susceptible)-1])}')
        # self.I_label_var.set(f'Veikir: {str(infected[len(infected)-1])}')
        # self.R_label_var.set(f'Náð bata: {str(removed[len(removed)-1])}')
        self.plot.cla()
        self.plot.stackplot(self.s.data.index.values,
                            self.s.data['I'],
                            self.s.data['S'],
                            self.s.data['R'],
                            colors=[COLORS['I'], COLORS['S'], COLORS['R']])

if __name__ == "__main__":
    app = Basis()
    app.title("COVID-19 hermun")
    app.resizable(False, False)
    app.mainloop()
