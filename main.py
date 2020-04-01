import numpy as np
import tkinter as tk
from tkinter import font  as tkfont

from options import *
from simulation import Simulation

class Basis(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=False)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.label = tk.Label(self, text="COVID-19 hermir", font = tkfont.Font(family='Helvetica', size=18, weight="bold"))
        self.canvas = tk.Canvas(self,
                           width=DIMENSIONS['width'],
                           height=DIMENSIONS['height'])

        self.label.pack(fill=tk.X)
        self.canvas.pack(fill=tk.X)
        self.canvas.config(bg="white")

        self.w_label = tk.Label(self, text="Fólksfjöldi", font = tkfont.Font(family='Helvetica', size=18, weight="normal"))
        self.w = tk.Scale(self, from_=50, to=150, orient="horizontal")
        self.w_label.pack(fill=tk.X)
        self.n0_label = tk.Label(self, text="Fjöldi smitaðra", font = tkfont.Font(family='Helvetica', size=18, weight="normal"))
        self.n0 = tk.Scale(self, from_=1, to=10, orient="horizontal")
        self.w.pack(fill=tk.X)
        self.n0_label.pack(fill=tk.X)
        self.n0.pack(fill=tk.X)
        self.b = tk.Button(self, text="Byrja", command= self.start_simulation)
        self.b.pack(fill = tk.X)
        self.c = tk.Button(self, text="Hætta", command=self.stop_simulation)
        self.c.configure(state='disabled')
        self.c.pack(fill = tk.X)

    def start_simulation(self):
        self.b.configure(state='disabled')
        self.w.configure(state='disabled')
        self.c.configure(state='normal')
        self.s = Simulation(self.canvas)
        self.s.simulate(self.w.get(), self.n0.get())

    def stop_simulation(self):
        self.b.configure(state='normal')
        self.w.configure(state='normal')
        self.s.cancel()
        self.canvas.delete('all')



if __name__ == "__main__":
    app = Basis()
    app.title("COVID-19 hermun")
    app.mainloop()
