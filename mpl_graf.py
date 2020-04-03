"""Keyra skránna í terminal með skipun: 
python3 mpl_graf.py &
python3 data.py &"""

import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('ggplot')

x_vals = []
y_vals = []

index = count()


def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['gogn_1']
    y2 = data['gogn_2']

    plt.cla()

    plt.plot(x, y1, label='Gögn 1')
    plt.plot(x, y2, label='Gögn 2')
    # plt.fill_between(x,y1,y2,color='r')
    # plt.fill_between(x,0,3,color='y')

    # plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=100)

plt.tight_layout()
plt.show()