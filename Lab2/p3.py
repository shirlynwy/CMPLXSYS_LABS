#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 21:57:42 2021

@author: shirlynw
"""

from math import *
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

g = nx.read_gml('polbooks/polbooks.gml')
pos = nx.spring_layout(g) # positions for all nodes

# =============================================================================
# nx.draw_networkx(g, pos, with_labels = False, node_size = 100) # draw network
# plt.show()
# =============================================================================

deg_seq = [d for n, d in g.degree()]
hist1 = np.histogram(deg_seq, bins = 'auto')
# =============================================================================
# print(hist1)
# print(hist1[0])
# print(hist1[1][1:end])
# =============================================================================

### 3a #################
# plt.figure()
# plt.hist(deg_seq, bins = 'auto')
# plt.title('Degree histogram')

# plt.figure()
# plt.plot(hist1[1][1:], hist1[0], 'b^-')
# plt.title('Number of nodes vs degree')

# plt.figure()
# plt.hist(np.log(deg_seq), bins = 'auto')
# plt.title('(Log) degree histogram')

# plt.figure()
# plt.plot(hist1[1][1:], np.log( hist1[0]), 'b^-')
# plt.title('Log(# of nodes) vs degree')
# plt.show()

###  3b  ###############

for k in range(3):
    if k == 0:
        mcolor = list(nx.closeness_centrality(g).values())
        mtitle = 'Closeness centrality'
    elif k == 1:
        mcolor = list(nx.degree_centrality(g).values())
        mtitle = 'Degree centrality'
    elif k == 2 :
        mcolor = list(nx.betweenness_centrality(g).values())
        mtitle = 'Betweeness centrality'
    elif k == 3:
        mcolor = list(nx.eigenvector_centrality(g).values())
        mtitle = 'Eigenvector centrality'

    plt.figure()
    nx.draw_networkx(g, pos, node_color= mcolor, node_size=200, with_labels = False, alpha=0.8, width = 2)
    plt.title(mtitle)
# plt.show()


n= g._node
colorkey = {'l': 'blue', 'c': 'red', 'n': 'grey'}
colors = [colorkey.get(n[x]['value'], 'green') for x in n]
plt.figure()
nx.draw_networkx(g, pos, node_color = colors, with_labels = False, node_size = 100, width = 2) # draw network
plt.title('Color by political party')


ast = nx.attribute_assortativity_coefficient(g, 'value')
#print(ast)

cmnt = nx.algorithms.community.greedy_modularity_communities(g)
#print(cmnt)

print(n['Allies'])
colorlist = [];
for x in n:
    if x in cmnt[0]:
        colorlist.append('red')
    elif x in cmnt[1]:
        colorlist.append('blue')
    elif x in cmnt[2]:
        colorlist.append('grey')
    else:
        colorlist.append('green')

plt.figure();
nx.draw_networkx(g, pos, node_color = colorlist, with_labels = False, node_size = 100, width = 2) # draw network
plt.title('Color by community')
plt.show()