import numpy as np
import tkinter as tk
from tkinter import font  as tkfont

from options import *

from queue import Queue

COLORS = {'S': '#9eedff',
          'I': '#ffc4b8',
          'R': '#91ffd7'
          }

class Simulation:
    def __init__(self, canvas):
        self.t = 0
        self.q = []
        self.next = None
        self.canvas = canvas


    def detectCollision(self, p, q):
        # Find the distance between two particles
        # dist = np.linalg.norm(p.r - q.r)
        dx = p.r[0] - q.r[0]
        dy = p.r[1] - q.r[1]
        dist = np.sqrt(dx**2 + dy**2)
        # sum_radius = p.radius*2
        sum_radius = RADIUS*2

        if dist < sum_radius:
            return True
        else:
            return False

    def changeDirection(self, dr):
        theta = np.arctan2(dr[1], dr[0])

        return np.array((np.cos(theta), np.sin(theta)))

    def collide(self, p, q):
        x = lambda a, b : a.v - (np.dot(a.v-b.v, a.r-b.r)/(np.linalg.norm(a.r - b.r)**2))*(a.r-b.r)
        p.v = x(p, q)
        q.v = x(q, p)
        # ar = self.changeDirection(q.r - p.r)
        # p.v -= ar
        # q.v = ar

        if p.status == "S" and q.status == "I":
            self.infect(p)
        elif q.status == "S" and p.status == "I":
            self.infect(q)

    def infect(self, particle):
        particle.status = "I"
        # Adds particle to queue with time + 5 sec
        self.q.append((self.t + TIME_TO_RECOVER, particle))

    def recover(self, particle):
        particle.status = "R"
        particle.hasMovement = False

    def addParticles(self, count):
        particles = []
        for i in range(count):
            hasMovement = False if np.random.uniform(100) < STATIC_PEOPLE_PERCENTAGE else True
            p = Particle(DIMENSIONS['width'] * np.random.rand(2),
                         (2*np.random.rand(2)-1) * 0.005,
                         COLORS['S'],
                         self.canvas,
                         hasMovement)
            particles.append(p)
        self.particles = particles

    def simulate(self, n):
        self.n = n
        # self.addParticles(NUMBER_OF_PEOPLE)
        self.addParticles(n)
        self.infect(self.particles[3])
        self.main()

    def main(self):
        w.configure(state='disabled')
        self.canvas.delete('all')
        # Update positions
        [particle.step() for particle in self.particles]

        order = np.random.permutation(self.n)
        # Do collisions
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                if self.detectCollision(self.particles[order[i]], \
                                        self.particles[order[j]]):
                    self.collide(self.particles[order[i]], \
                                 self.particles[order[j]])
                    break


        self.t += 1
        for event in self.q:
            if event[0] == self.t:
                self.recover(event[1])

        self._job = self.canvas.after(2, self.main)

    def cancel(self):
        w.configure(state='normal')
        canvas.after_cancel(self._job)
        self.canvas.delete('all')


# Takes in r=np.array((x,y)), v.np.array((vx,vy))
class Particle:
    def __init__(self, r, v, color, canvas, hasMovement = True):
        self.r = r
        self.v = v
        self.status = "S"
        self.hasMovement = hasMovement
        self.canvas = canvas

    def step(self):
        self.shape = self.canvas.create_oval(self.r[0] - RADIUS,
                                        self.r[1] - RADIUS,
                                        self.r[0] + RADIUS,
                                        self.r[1] + RADIUS,
                                        fill = COLORS[self.status])
        if not self.hasMovement:
            return

        # Collide with walls
        if self.r[0] < 0 or self.r[0] > DIMENSIONS['width']:
            self.v[0] = -self.v[0]
        if self.r[1] < 0 or self.r[1] > DIMENSIONS['height']:
            self.v[1] = -self.v[1]
        self.r += self.v*SPEED
        # self.canvas.move(self.shape, self.v[0]*SPEED, self.v[1]*SPEED)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("COVID-19 hermir")
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew")
    label = tk.Label(frame, text="COVID-19 hermir", font = tkfont.Font(family='Helvetica', size=18, weight="bold"))
    canvas = tk.Canvas(frame,
                       width=DIMENSIONS['width'],
                       height=DIMENSIONS['height'])

    frame.pack(fill=tk.X)
    label.pack(fill=tk.X)
    canvas.pack(fill=tk.X)
    canvas.config(bg="white")

    w_label = tk.Label(frame, text="Fólksfjöldi", font = tkfont.Font(family='Helvetica', size=18, weight="normal"))
    w = tk.Scale(frame, from_=50, to=250, orient="horizontal")
    w_label.pack(fill=tk.X)
    w.pack(fill=tk.X)
    s = Simulation(canvas)
    b = tk.Button(frame, text="Byrja", command= lambda: s.simulate(w.get()))
    b.pack(fill = tk.X)
    c = tk.Button(frame, text="Hætta", command=s.cancel)
    c.pack(fill = tk.X)

    root.mainloop()
