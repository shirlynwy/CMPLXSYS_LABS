#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 23:01:50 2020

@author: marisaeisenberg
"""

import pycxsimulator
from pylab import *

n = 100 # size of space: n x n
p = 0.5 # probability of voting yes

def initialize():    
    global config, nextconfig  # Things we need to access from different functions go here (discuss globals)
    
    # Build our grid of agents - fill with zeros for now
    config = zeros([n, n])
    
    # Set them to vote yes with probability p
    for x in range(n):
        for y in range(n):
            if random() < p: config[x, y] = 1
            
    # Set the next timestep to zeros for now (we will update in the update function)
    nextconfig = zeros([n, n])
    

def update():
    global config, nextconfig
    
    # Go through each cell and check if they should change their vote in the next step
    for x in range(n):
        for y in range(n):
            count = 0  # variable to keep track of how many neighbors are voting yes
            for dx in [-1, 0, 1]:       # check the cell before/middle/after
                for dy in [-1, 0, 1]:   # check above/middle/below (discuss nesting for loops vs. not here)
                    # Add to count if neighbor is voting yes (note you also count yourself!)
                    count += config[(x + dx) % n, (y + dy) % n] # discuss 
                    
            # Now that we know how many neighbors are voting yes, decide what to do
            if config[x,y] == 0: # if this agent was going to vote no
                nextconfig[x, y] = 1 if count > 4 else 0 # note we only change the vote for nextconfig, not config!
            else: # otherwise this agent must have been going to vote yes (could also do elif)
                nextconfig[x, y] = 0 if (8 - (count-1)) > 4 else 1  #reduce count by 1 since counted self
            
    config, nextconfig = nextconfig, zeros([n, n])
    # Can also be a little more efficient and do config, nextconfig = nextconfig, config, but be careful

def observe():
    global config, nextconfig
    cla()
    imshow(config, vmin = 0, vmax = 1, cmap = cm.binary)
    

pycxsimulator.GUI().start(func=[initialize, observe, update])

