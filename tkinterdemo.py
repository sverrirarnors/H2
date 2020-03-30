import numpy as np
import tkinter as tk
import random as rm

class particle:
    def __init__(self, p, v, a=np.array([0,10]), colour="blue"):
        self.shape = canvas.create_oval(p[0]-2, p[1]-2, p[0]+2, p[1]+2, fill = colour)
        self.p = np.array([float(i) for i in p]) #position
        self.v =np.array([float(i) for i in v]) #velocity
        self.oldv = np.copy(v)
        self.a = np.array([float(i) for i in a]) # accelleration
        self.colour = colour

    def update(self, delay):
        self.v += self.a*delay
        self.p += (self.v*delay)
        canvas.move(self.shape, self.v[0]*delay, self.v[1]*delay)

        if not 0<self.p[0]<800: #keeps it within boundaries
            self.v *= np.array([-1,1])
        if not 0<self.p[1]<400:
            self.v *= np.array([1,-1])

    def collide(self, other):
        x = self.p-other.p
        mag = np.sqrt(x.dot(x)) # checks distance
        if 0<mag<4:
            self.oldv = np.copy(self.v)
            x /= mag

            inline = x*x.dot(self.v)
            inlineo = x*x.dot(other.oldv)

            self.v -= inline - inlineo

#---------------------------------------------------------------------------------

def main():
    [i.update(Time_per_frame) for i in particles]

    [[j.collide(i) for i in particles] for j in particles]

    canvas.after(int(Time_per_frame*1000),main)

#---------------------------------------------------------------------------------
#creates the window
root = tk.Tk()
root.title("Ball Bouncer")
root.resizable(False,False)
canvas = tk.Canvas(root, width = 800, height = 400)
canvas.pack()
canvas.config(bg="white")

#---------------------------------------------------------------------------------
#set variables
Time_per_frame = 0.02
NoParticles = 100
particles = [particle([rm.randint(100,700),rm.randint(100,300)], [rm.randint(-100,100),rm.randint(-100,100)],[0,0]) for i in range(100)]
#particles = [particle([50,53],[50,0],[0,0]),particle([150,50],[-50,0],[0,0])]

#---------------------------------------------------------------------------------

main()

root.mainloop()
