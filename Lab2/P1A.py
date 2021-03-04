#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 17:34:09 2021

@author: shirlynw
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from math import *

import warnings
warnings.filterwarnings("ignore")

g = nx.DiGraph() # Make an empty graph that will be the phase space
L = 8 #9 #10     # Grid size (start with something small)

# Rule 50
neighrule = {
        (0,0,0):0,
        (0,0,1):1,
        (0,1,0):0,
        (0,1,1):0,
        (1,0,0):1,
        (1,0,1):1,
        (1,1,0):0,
        (1,1,1):0
        }


# Takes a configuration and returns the corresponding integer
def config2int(config):
    return int(''.join(map(str, config)),2) #maps the config->strings, joins them, and then converts to int from binary

# Takes an integer and converts it to a configuration (list of cell states)
def int2config(x):
    return [1 if x & 2**i > 0 else 0 for i in range(L - 1, -1, -1)]

# =============================================================================
# z = config2int([0,1,0,0,1,1])
# print(z)
# =============================================================================

# Function to update the CA one timestep
def update(config):
    nextconfig = [0]*L
    for x in range(L):
        nextconfig[x] = neighrule[(config[(x - 1) % L],config[x],config[(x + 1) % L])]
    return nextconfig


# Go through every possible configuration and add an edge linking it to where it goes next
for x in range(2**L):
    g.add_edge(x, config2int(update(int2config(x))))
    

# Plot each connected component of the phase space
ccs = [cc for cc in nx.connected_components(g.to_undirected())]
n = len(ccs)
w = ceil(sqrt(n))
h = ceil(n / w)

plt.figure(0)
for i in range(n):
    plt.subplot(h, w, i + 1)
    nx.draw_networkx(nx.subgraph(g, ccs[i]), with_labels = True)
#plt.show()


# Plot each component with the attracting subcomponent highlighted
for i in range(n):
    j = i % 4
    if j == 0:
        plt.figure()
    plt.subplot(2, 2, j + 1)
    subg = nx.subgraph(g, ccs[i])
    attr = set().union(*nx.attracting_components(subg))

    pos=nx.spring_layout(subg) # positions for all nodes
    nx.draw_networkx_nodes(subg, pos, nodelist = attr, node_color='r', node_size=500, alpha=0.8)
    nx.draw_networkx_nodes(subg,pos, nodelist = (set(subg.nodes()) - attr), node_color='#00b4e9', node_size=500, alpha=0.8)
    nx.draw_networkx_edges(subg,pos,width=2.0)
    nx.draw_networkx_labels(subg,pos)

#large attraction basin, centrality meansure

subg = nx.subgraph(g, ccs[1])
#attr = set().union(*nx.attracting_components(subg))


# =============================================================================
# nx.draw_networkx_nodes(subg, pos, nodelist = attr, node_color= temp, node_size=500, alpha=0.8)
# #nx.draw_networkx_nodes(subg,pos, nodelist = (set(subg.nodes()) - attr), node_color='#00b4e9', node_size=500, alpha=0.8)
# nx.draw_networkx_edges(subg,pos,width=2.0)
# nx.draw_networkx_labels(subg,pos)
# =============================================================================
pos=nx.random_layout(subg) # positions for all nodes
for k in range(4):
    if k == 0:
        mcolor = list(nx.closeness_centrality(subg).values())
    elif k == 1:
        mcolor = list(nx.degree_centrality(subg).values())
    elif k == 2 :
        mcolor = list(nx.betweenness_centrality(subg).values())
    elif k == 3:
        mcolor = list(nx.eigenvector_centrality(subg).values())

    plt.figure()
    nx.draw_networkx(subg, pos, node_color= mcolor, with_labels = True, node_size=400, alpha=0.8)

# Check if cycles
# =============================================================================
# aha = list(nx.simple_cycles(nx.subgraph(g,ccs[1])))
# print(aha)
# =============================================================================

# Plot the CA behavior starting at an interesting IC from the above
# Run the model for a few steps and plot
plt.figure()
steps = 20
output = np.zeros([steps,L])
output[0,:] = int2config(11)
for i in range(1,steps):
    output[i,:] = update(output[i-1,:])
plt.cla()
plt.imshow(output)
plt.show()