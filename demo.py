import pygame

from math import hypot
from random import randint, shuffle


class Circle:

    def __init__(self, x, y, radius, dx, dy, color):

        self.x = x
        self.y = y
        self.r = radius
        self.dx = dx
        self.dy = dy
        self.color = color

    def render(self):

        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.r)


def randomColor():

    r = randint(0, 255)
    g = randint(0, 255 - r)
    b = 255 - r - g
    color = [r, g, b]
    shuffle(color)

    return color


def detectCollision(a, b):

    d = hypot(a.x - b.x, a.y - b.y)
    r = a.r + b.r

    if (d < r):
        return True
    else:
        return False


def backProjection(ax, ay, bx, by):

    e1 = (1.0, 0.0)
    a1 = ax * e1[0] + ay * e1[1]
    b1 = bx * e1[0] + by * e1[1]
    f1 = a1 + b1

    e2 = (0.0, 1.0)
    a2 = ax * e2[0] + ay * e2[1]
    b2 = bx * e2[0] + by * e2[1]
    f2 = a2 + b2

    return (f1, f2)


def orthProjection(ax, ay, bx, by):

    f = float(ax * bx + ay * by)
    f = f / float(bx * bx + by * by)

    return (f * bx, f * by)


def positionUpdate(a, b):

    mx = (a.x + b.x) / 2
    my = (a.y + b.y) / 2

    d = hypot(a.x - mx, a.y - my)

    ex = (a.x - mx) / d
    ey = (a.y - my) / d

    a.x = mx + ex * a.r
    a.y = my + ey * a.r

    ex = -ex
    ey = -ey

    b.x = mx + ex * b.r
    b.y = my + ey * b.r

    return a, b


def solveCollision(a, b):

    sz = (a.x - b.x, a.y - b.y)
    st = (-sz[1], sz[0])

    a_sz = orthProjection(a.dx, a.dy, sz[0], sz[1])
    a_st = orthProjection(a.dx, a.dy, st[0], st[1])
    b_sz = orthProjection(b.dx, b.dy, sz[0], sz[1])
    b_st = orthProjection(b.dx, b.dy, st[0], st[1])

    a.dx, a.dy = backProjection(b_sz[0], b_sz[1], a_st[0], a_st[1])
    b.dx, b.dy = backProjection(a_sz[0], a_sz[1], b_st[0], b_st[1])

    a, b = positionUpdate(a, b)

    return a, b


def step(circle):

    circle.x = circle.x + circle.dx
    circle.y = circle.y + circle.dy

    if circle.x > 800:
        circle.dx = -circle.dx
        circle.x = 800 + 800 - circle.x
    if circle.x < 0:
        circle.dx = -circle.dx
        circle.x = 0 + 0 - circle.x
    if circle.y > 600:
        circle.dy = -circle.dy
        circle.y = 600 + 600 - circle.y
    if circle.y < 0:
        circle.dy = -circle.dy
        circle.y = 0 + 0 - circle.y

    return circle


pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

circles = []
for x in range(0, 100):
    circle = Circle(100 + x * 50, 50 + x * 50, 10, randint(-5, 5), randint(-5, 5), randomColor())
    circles.append(circle)

gameLoop = True

while gameLoop:

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            gameLoop = False

    circles = [step(circle) for circle in circles]

    for a in range(0, len(circles)):
        for b in range(a + 1, len(circles)):
            if detectCollision(circles[a], circles[b]):
                circles[a], circles[b] = solveCollision(circles[a], circles[b])
                break

    window.fill((255, 255, 255))

    [circle.render() for circle in circles]

    pygame.display.flip()

    clock.tick(50)

pygame.quit()
