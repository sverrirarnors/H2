import tkinter as tk
from options import COLORS

# For plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Dashboard(tk.Frame):
    def __init__(self, controller, parent):
        tk.Frame.__init__(self, master=parent)
        self.controller = controller

        # Graph
        self.fig = plt.Figure()
        self.plot = self.fig.add_subplot(111)
        self.plot.axes.get_xaxis().set_visible(False)
        self.plot.axes.get_yaxis().set_visible(False)
        self.graph = FigureCanvasTkAgg(self.fig, master=self)
        self.graph.get_tk_widget().grid(column=1, columnspan=2, rowspan=2, row=1)
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=100)

        self.stats_container = tk.Frame(master=self)
        self.S_label_var = tk.StringVar(self)
        self.S_label = tk.Label(self.stats_container, textvariable=self.S_label_var)
        self.S_label.pack(anchor=tk.W)

        self.I_label_var = tk.StringVar(self)
        self.I_label = tk.Label(self.stats_container, textvariable=self.I_label_var)
        self.I_label.pack(anchor=tk.W)

        self.R_label_var = tk.StringVar(self)
        self.R_label = tk.Label(self.stats_container, textvariable=self.R_label_var)
        self.R_label.pack(anchor=tk.W)

        self.rt_label_var = tk.StringVar(self)
        self.rt_label = tk.Label(self.stats_container, textvariable=self.rt_label_var)
        self.rt_label.pack(anchor=tk.W)

        self.stats_container.grid(row=3, column=1)

    def animate(self, i):
        data = self.controller.s.data
        self.rt_label_var.set(f'Meðaltals RT: {self.controller.s.average_rt:.2f}')
        self.S_label_var.set(f'Heilbrigðir: {int(data["S"].iloc[-1])}')
        self.I_label_var.set(f'Veikir: {int(data["I"].iloc[-1])}')
        self.R_label_var.set(f'Náð bata: {int(data["R"].iloc[-1])}')
        self.plot.cla()
        self.plot.stackplot(self.controller.s.data['x'],
                            self.controller.s.data['I'],
                            self.controller.s.data['S'],
                            self.controller.s.data['R'],
                            colors=[COLORS['I'], COLORS['S'], COLORS['R']])
