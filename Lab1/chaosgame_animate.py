#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 22:54:40 2021

@author: shirlynw
"""

#chaos_game.py
from math import *                  # useful math functions
import numpy as np                  # useful array objects 
                                    # (also a core scientific computing library)
import matplotlib.pyplot as plt     # nice plotting commands
from matplotlib import animation
from random import random, randint  # random number generation functions

#global variables
N = 1000;
corner= [[0,0], [1,0], [0.5, sqrt(3)/2]]

"""
def midpoint (point1, point2):
    midpoint = [ 0.5 * (point1[0] + point2[0]) , 0.5 * (point1[1] + point2[1])]
    return midpoint



#define variables
x = np.zeros(N)
y = np.zeros(N)

x[0] = random()
y[0] = random()

for i in range(1,N-1):
    choose = random()
    if choose <=1/3:
        i_corner = [0,0]
    elif (choose > 1/3 )and (choose <=2/3):
        i_corner = [1,0]
    else:
        i_corner = [0.5, sqrt(3)/2]

    newxy = midpoint((x[i-1],y[i-1]),i_corner)
    x[i] = newxy[0]
    y[i] = newxy[1]
    #im = plt.scatter(x, y, color = 'blue')
   

fig = plt.figure()
plt.scatter(x, y, color = 'blue')
plt.scatter((0,1,0.5), (0,0,sqrt(3)/2), color = 'red')
plt.show()
"""
def midpoint (point1, point2):
    midpoint = [ 0.5 * (point1[0] + point2[0]) , 0.5 * (point1[1] + point2[1])]
    return midpoint


fig = plt.figure()
ax = plt.axes(xlim=(-0.1, 1.1), ylim=(-0.1, 1))
dots, = ax.plot([], [], 'bo')


# initialization function: plot the background of each frame
def init():
    global x,y
    x = np.zeros(N)
    y = np.zeros(N)
    plt.scatter((0,1,0.5), (0,0,sqrt(3)/2), color = 'red')
    return dots,

# animation function.  This is called sequentially
def animate(i):
    if i ==0:
        x[0] = random()
        y[0] = random()
    else: 
        choose = random()
        if choose <=1/3:
            i_corner = [0,0]
        elif (choose > 1/3 )and (choose <=2/3):
            i_corner = [1,0]
        else:
            i_corner = [0.5, sqrt(3)/2]

        newxy = midpoint((x[i-1],y[i-1]),i_corner)
        x[i] = newxy[0]
        y[i] = newxy[1]
    
    dots.set_data(x, y)
    return dots,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=1000, interval=5, blit=True, repeat = False)


anim.save('chaos_vid.mp4', fps=80, extra_args=['-vcodec', 'libx264'])
plt.show()