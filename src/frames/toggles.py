import tkinter as tk
from tkinter import font as tkfont
from simulation import Simulation


# Frame for toggles
class Toggles(tk.Frame):
    def start_simulation(self):
        self.begin.configure(state='disabled')
        self.pop.configure(state='disabled')
        self.n0.configure(state='disabled')
        self.mobility.configure(state='disabled')
        self.stop.configure(state='normal')
        self.collisions_checkbox.configure(state='disabled')
        self.controller.s = Simulation(self, self.controller.canvas)
        self.controller.s.simulate(self.pop.get(),
                                   self.n0.get(),
                                   self.mobility.get(),
                                   self.collections.get(),
                                   self.collisions_var.get())


    def stop_simulation(self):
        self.begin.configure(state='normal')
        self.pop.configure(state='normal')
        self.n0.configure(state='normal')
        self.mobility.configure(state='normal')
        self.stop.configure(state='disabled')
        self.collisions_checkbox.configure(state='normal')
        self.controller.s.stop()
        self.controller.canvas.delete('all')

    def __init__(self, controller, parent):
        tk.Frame.__init__(self, master=parent)
        self.controller = controller


        # Population-slider
        self.pop_label = tk.Label(self,
                                  text="Fólksfjöldi",
                                  font=tkfont.Font(family='Helvetica',
                                  size=18,
                                  weight="normal"))
        self.pop_label.grid(row=1, columnspan=2, pady=10)
        self.pop = tk.Scale(self, from_=100, to=500, orient="horizontal")
        self.pop.grid(row=2, columnspan=2)

        # Number of infected
        self.n0_label = tk.Label(self,
                                 text="Fjöldi smitaðra",
                                 font=tkfont.Font(family='Helvetica',
                                 size=18,
                                 weight="normal"))
        self.n0 = tk.Scale(self, from_=2, to=10, orient="horizontal")
        self.n0_label.grid(row=1, column=2)
        self.n0.grid(row=2, column=2)

        # Mobility
        self.mobility_label = tk.Label(self,
                                       text="Hlýða Víði (%)",
                                       font=tkfont.Font(family='Helvetica',
                                       size=18,
                                       weight="normal"))

        self.mobility = tk.Scale(self, from_=0, to=100, orient="horizontal")
        self.mobility_label.grid(row=1, column=3)
        self.mobility.grid(row=2, column=3)

        # Collections
        collections = [('1', 1), ('2', 2), ('4',4)]
        self.collections = tk.IntVar()
        self.collections_label = tk.Label(self,
                                          text="Fjöldi hólfa",
                                          font=tkfont.Font(family='Helvetica',
                                          size=18,
                                          weight="normal"))

        self.collections_label.grid(row=1, column=4)
        self.collections_frame = tk.Frame(self)
        self.collections_frame.grid(row=2, column=4)
        for val, num in collections:
            tk.Radiobutton(self.collections_frame,
                           text=num,
                           variable=self.collections,
                           value=val).pack(side='left', anchor=tk.W)

        self.collisions_var = tk.BooleanVar(value=True)
        self.collisions_checkbox= tk.Checkbutton(self, text="Árekstrar", variable=self.collisions_var)
        self.collisions_checkbox.grid(row=4, column=2)

        # Start and stop
        self.begin = tk.Button(self, text="Byrja", command=self.start_simulation, width=10)
        self.begin.grid(row=3, column=2, pady=20)
        self.stop = tk.Button(self, text="Hætta", command=self.stop_simulation, width=10)
        self.stop.configure(state='disabled')
        self.stop.grid(row=3, column=3)
