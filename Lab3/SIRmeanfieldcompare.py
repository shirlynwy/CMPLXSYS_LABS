#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparison of SIR dynamics on a network vs. difference equation mean-field model

Created on Thu Feb 20 14:35:39 2020

@author: marisaeisenberg
"""


import pycxsimulator
from pylab import *

import networkx as nx

N = 100 #100 #200  #1000

p_e = 0.05 # probability of edge generation
p_i = 0.12 # 0.5 # infection probability per contact
p_r = 0.1  # recovery probability

R0 = (N-1)*p_e*p_i/p_r

prev = []    # prevalence (total infected nodes/total nodes) in the network model
prev_mf = [] # prevalence (total infected nodes/total nodes) in the mean field model
susc_mf = [] # fraction of nodes that are susceptible in the mean field model


def initialize():
    global g, nextg, prev, prev_mf, susc_mf
    
    # Initialize network model
    g = nx.erdos_renyi_graph(N,p_e)        # start with an ER graph
    g.pos = nx.spring_layout(g)
    nx.set_node_attributes(g, 0, 'state')  # everyone starts off susceptible
    g._node[1]['state'] = 1                 # set one node to be infected (index case)
    nextg = g.copy()
    nextg.pos = g.pos
    prev.append(1/len(g._node))            # initial prevalence (fraction infected) in the network
    
    # Initialize mean field model
    susc_mf.append((N-1)/N) # initial susceptible fraction in the mean field model
    prev_mf.append(1/N)     # initial prevalence (fraction infected) in the mean field model
    

def update():
    global g, nextg, prev, prev_mf, susc_mf
    
    # Update network model
    curprev = 0
    nextg = g.copy()
    nextg.pos = g.pos
    for a in g._node:
        if g._node[a]['state'] == 0: # if susceptible
            nextg._node[a]['state'] = 0
            for b in g.neighbors(a):
                if g._node[b]['state'] == 1: # if neighbor b is infected
                    if random() < p_i:
                        nextg._node[a]['state'] = 1  # become infected with probability p_i
        elif g._node[a]['state'] ==1: # if infected
            curprev += 1
            nextg._node[a]['state'] = 2 if random() < p_r else 1  # recover with probability p_r
    prev.append(curprev/len(g._node))
    g = nextg.copy()
    g.pos = nextg.pos
    
    # Update mean field model (see class notes for equations)
    susc_mf.append(susc_mf[-1] - (N-1)*p_e*p_i*prev_mf[-1]*susc_mf[-1])
    prev_mf.append(prev_mf[-1] + (N-1)*p_e*p_i*prev_mf[-1]*susc_mf[-1] - p_r*prev_mf[-1])
    
    
def observe():
    global g, prev, prev_mf, susc_mf
    cla()
    nx.draw(g, cmap = cm.Wistia, vmin = 0, vmax = 2,
            node_color = [g._node[i]['state'] for i in g._node],
            pos = g.pos)

pycxsimulator.GUI().start(func=[initialize, observe, update])


# After we run the simulation, compare the mean field and network models
epicurve = scatter(range(len(prev)), prev)
scatter(range(len(prev_mf)), prev_mf)
xlabel("Time")
ylabel("Prevalence")
show(epicurve)

# Print the R0 for this simulation
print(R0)





