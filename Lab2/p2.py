#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:28:24 2021

@author: shirlynw
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 23:01:50 2020

@author: marisaeisenberg
"""

import pycxsimulator
from pylab import *


n = 11 # size of space: n x n
antmarker = {0:'^', 1:'>', 2:'v', 3:'<'}
#ant = [5,5,0]


def initialize():    
    global config, nextconfig  # Things we need to access from different functions go here (discuss globals)
    global ant 
    ant = [n //2 ,n //2 ,0]
    # Build our grid of agents - fill with zeros for now
    config = zeros([n, n])
    
    # Set them to vote yes with probability p
# =============================================================================
#     for x in range(n):
#         for y in range(n):
#             if random() < p: config[x, y] = 1
# =============================================================================
            
    # Set the next timestep to zeros for now (we will update in the update function)
    nextconfig = zeros([n, n])

    

def update():
    
    
# =============================================================================
#     # Go through each cell and check if they should change their vote in the next step
#     for x in range(n):
#         for y in range(n):
#             count = 0  # variable to keep track of how many neighbors are voting yes
#             for dx in [-1, 0, 1]:       # check the cell before/middle/after
#                 for dy in [-1, 0, 1]:   # check above/middle/below (discuss nesting for loops vs. not here)
#                     # Add to count if neighbor is voting yes (note you also count yourself!)
#                     count += config[(x + dx) % n, (y + dy) % n] # discuss 
#                     
#             # Now that we know how many neighbors are voting yes, decide what to do
#             if config[x,y] == 0: # if this agent was going to vote no
#                 nextconfig[x, y] = 1 if count > 4 else 0 # note we only change the vote for nextconfig, not config!
#             else: # otherwise this agent must have been going to vote yes (could also do elif)
#                 nextconfig[x, y] = 0 if (8 - (count-1)) > 4 else 1  #reduce count by 1 since counted self
# 
# =============================================================================

    global config, nextconfig            
    
    
    nextconfig = config

    if config[ant[0], ant[1]] == 1: #black tile
        nextconfig[ant[0], ant[1]] = 0
        ant[2] = (ant[2] + 1) % 4   #turn right 
    else: #white tile
        nextconfig[ant[0], ant[1]] = 1
        ant[2] = (ant[2] - 1) % 4        #turn left
    
    
    face = ant[2]
    x = ant[0]
    y = ant[1]
    if face == 0: #face up
        ant[0]  = (x - 1) % n
        
        #ant[0:1] = [(ant[0]-1) % n, ant[1]]
    elif face == 1: #face right
        ant[1] = (y+1) % n
        #ant[0:1] = [ant[0], (ant[1]+1) % n]
    elif face == 2: #face down
        ant[0] = (x+1) % n
        #ant[0:1] = [(ant[0]+1) % n, ant[1]]
    else: #face left
        ant[1] = (y-1) % n
        #ant[0:1] = [ant[0], (ant[1]-1) % n]
    
  
    #scatter(ant[1], ant[0], c='red', marker=antmarker[ant[2]])        
    config = nextconfig
    # Can also be a little more efficient and do config, nextconfig = nextconfig, config, but be careful

def observe():
    global config, nextconfig
    cla()
    imshow(config, vmin = 0, vmax = 1, cmap = cm.binary)
    scatter(ant[1], ant[0], s=30, c='red', marker=antmarker[ant[2]]) 

    



pycxsimulator.GUI().start(func=[initialize, observe, update])

