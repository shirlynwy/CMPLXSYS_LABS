#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# """
# Created on Sun Mar 28 17:45:12 2021

# @author: yixuanwang
# """


# import pycxsimulator
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


from pylab import *
from scipy.special import comb
N = 100 #100 #200  #1000

p_e = 0.06 # probability of edge generation
p_i = 0.1 # 0.5 # infection probability per contact
p_r = 0.1  # recovery probability

R0 = (N-1)*p_e*p_i/p_r



edge_num = np.floor(comb(N, 2) * p_e)
k = round(edge_num * 2 / N)
beta = 0.5

timesteps = 100
numsims = 100
prevarray = np.zeros([timesteps, numsims])
# prev_mf = [] # prevalence (total infected nodes/total nodes) in the mean field model
def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


def initialize():
    global g, nextg, prev, prev_mf, susc_mf
    prev = []    # prevalence (total infected nodes/total nodes) in the network model
    prev_mf = [] # prevalence (total infected nodes/total nodes) in the mean field model
    susc_mf = [] # fraction of nodes that are susceptible in the mean field model
    
       # Initialize network model
    g = nx.watts_strogatz_graph(N,k, beta)        # start with an ER graph
    # g = nx.erdos_renyi_graph(N,p_e)   
    g.pos = nx.circular_layout(g)
    nx.set_node_attributes(g, 0, 'state')  # everyone starts off susceptible
    g._node[1]['state'] = 1                 # set one node to be infected (index case)
    nextg = g.copy()
    nextg.pos = g.pos
    prev.append(1/len(g._node))            # initial prevalence (fraction infected) in the network
    
    # Initialize mean field model
    susc_mf.append((N-1)/N) # initial susceptible fraction in the mean field model
    prev_mf.append(1/N)     # initial prevalence (fraction infected) in the mean field modelel
    

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
    
    
# def observe():
#     global g, prev, prev_mf, susc_mf
#     cla()
#     nx.draw(g, cmap = cm.Wistia, vmin = 0, vmax = 2,
#             node_color = [g._node[i]['state'] for i in g._node],
#             pos = g.pos)



for i in range(0,numsims):        # loop over all simulations
    initialize()                  # initialize each simulation
    for j in range(1,timesteps):  # loop over the timesteps for that simulation
        update()                  # update
    prevarray[:,i] = prev         # store the resulting simulation in prevarray




# =============================================================================
# =============================================================================
# 
# ### After we run the simulation, compare the mean field and network models
# plt.figure()
# # epicurve = scatter(range(len(prev)), prev)
# ax = plt.gca()
# ### scatter plot and Erdos-Renyi mean field
# for i in range(0, numsims):
#     prev1 = prevarray[:, i] 
#     ax.scatter(range(len(prev1)), prev1, s = 3)
#     # plt.hold('True')
#     # ax.legend()
# 
# plt.plot(range(len(prev_mf)), prev_mf,  linewidth = 4, color='black')
# 
# plt.xlabel("Time")
# plt.ylabel("Prevalence")
# plt.show(block=True)
# =============================================================================
# =============================================================================


#### plot quantiles
# sorted_prev = prevarray.sort(axis=0)
median_array = np.quantile(prevarray, 0.5, axis=1)
quant5_array = np.quantile(prevarray, 0.05, axis=1)
quant25_array = np.quantile(prevarray, 0.25, axis=1)
quant75_array = np.quantile(prevarray, 0.75, axis=1)
quant95_array = np.quantile(prevarray, 0.95, axis=1)

# =============================================================================
# plt.figure()
# plt.plot(range(len(quant5_array)), quant5_array, linewidth = 2, label = '5th quntile')
# plt.plot(range(len(quant25_array)), quant25_array, linewidth = 2, label = '25th quntile')
# plt.plot(range(len(median_array)), median_array, linewidth = 2, label = 'median')
# plt.plot(range(len(quant75_array)), quant75_array, linewidth = 2, label = '75th quntile')
# plt.plot(range(len(quant95_array)), quant95_array, linewidth = 2, label = '95th quntile')
# 
# plt.legend()
# =============================================================================

# plt.show(block = True)

# plt.figure()

# plt.plot(quant5_array, linewidth = 2, label = '5th quntile')

# plt.plot(range(len(quant25_array)), quant25_array, linewidth = 2, label = '25th quntile')
# plt.legend()

# plt.show(block = True)

plt.figure()
plt.fill_between(range(len(quant5_array)), quant5_array, quant95_array, color=lighten_color('b', 0.7))
plt.fill_between(range(len(quant5_array)), quant25_array, quant75_array, color=lighten_color('b', 0.3))
plt.plot(range(len(median_array)), median_array, color = 'blue', linewidth = 4, label = 'median')
plt.plot(range(len(prev_mf)), prev_mf,  linewidth = 4, color='black')
plt.show(block = True)