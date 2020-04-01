COLORS = {'S': '#9eedff',
          'I': '#ffc4b8',
          'R': '#91ffd7'
          }

from options import RADIUS, DIMENSIONS
# Takes in r=np.array((x,y)), v.np.array((vx,vy))
class Particle:
    def __init__(self, r, v, color, canvas, hasMovement = True):
        self.r = r
        self.v = v
        self.status = "S"
        self.hasMovement = hasMovement
        self.canvas = canvas

    def step(self):
        self.shape = self.canvas.create_oval(self.r[0]*DIMENSIONS['width'] - RADIUS,
                                        self.r[1]*DIMENSIONS['height'] - RADIUS,
                                        self.r[0]*DIMENSIONS['width'] + RADIUS,
                                        self.r[1]*DIMENSIONS['height'] + RADIUS,
                                        fill = COLORS[self.status])
        if not self.hasMovement:
            return

        # Collide with walls
        if self.r[0] < 0 or self.r[0] > 1:
            self.v[0] = -self.v[0]
        if self.r[1] < 0 or self.r[1] > 1:
            self.v[1] = -self.v[1]
            
        self.r += self.v
