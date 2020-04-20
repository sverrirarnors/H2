import tkinter as tk
from tkinter import font  as tkfont

from options import DIMENSIONS
from simulation import Simulation

#Import frames
from frames.dashboard import Dashboard
from frames.toggles import Toggles

class Basis(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.pack()

        self.left_div = tk.Frame(master=self.container)
        self.right_div = tk.Frame(master=self.container)

        self.left_div.pack(side='left', anchor=tk.W)
        self.right_div.pack(side='left', anchor=tk.W)

        self.canvas = tk.Canvas(self.left_div,
                           width=DIMENSIONS['width'],
                           height=DIMENSIONS['height'], borderwidth=2, relief='solid')

        self.canvas.grid(row=2, columnspan=4)
        self.canvas.config(bg="white")
        self.s = Simulation(self, self.canvas)


        self.toggles = Toggles(controller=self, parent=self.right_div)
        self.toggles.pack()
        self.dashboard = Dashboard(controller=self, parent=self.right_div)
        self.dashboard.pack()

if __name__ == "__main__":
    app = Basis()
    app.title("COVID-19 hermir")
    app.resizable(False, False)
    app.mainloop()
