import pycxsimulator
from pylab import *
import matplotlib.pyplot as plt
import numpy as np


import copy as cp

# nr = 500. # carrying capacity of rabbits

r_init = 100 # initial rabbit population
mr = 0.03 # magnitude of movement of rabbits
dr = 1.0 # death rate of rabbits when it faces foxes
rr = 0.1 # reproduction rate of rabbits

f_init = 30 # initial fox population
mf = 0.05 # magnitude of movement of foxes
df = 0.1 # death rate of foxes when there is no food
rf = 0.5 # reproduction rate of foxes

cd = 0.02 # radius for collision detection
cdsq = cd ** 2


numsims = 6
N = 400

nr_list = range(200, 850, 50)
# print(list(nr_list))
# print(nr_list[-1])

r_final_avg= np.zeros(len(nr_list))
f_final_avg= np.zeros(len(nr_list))

class agent:
    pass

def initialize():
    global agents, rdata, fdata, iscontinue
    agents = []
    rdata = []
    fdata = []
    iscontinue = 1
    for i in range(r_init + f_init):
        ag = agent()
        ag.type = 'r' if i < r_init else 'f'
        ag.x = random()
        ag.y = random()
        agents.append(ag)

def observe():
    global agents, rdata, fdata

    subplot(2, 1, 1)
    cla()
    rabbits = [ag for ag in agents if ag.type == 'r']
    if len(rabbits) > 0:
        x = [ag.x for ag in rabbits]
        y = [ag.y for ag in rabbits]
        plot(x, y, 'b.')
    foxes = [ag for ag in agents if ag.type == 'f']
    if len(foxes) > 0:
        x = [ag.x for ag in foxes]
        y = [ag.y for ag in foxes]
        plot(x, y, 'ro')
    axis('image')
    axis([0, 1, 0, 1])

    subplot(2, 1, 2)
    cla()
    plot(rdata, label = 'prey')
    plot(fdata, label = 'predator')
    legend()

def update_one_agent():
    global agents
    if agents == []:
        return

    ag = choice(agents)

    # simulating random movement
    m = mr if ag.type == 'r' else mf
    ag.x += uniform(-m, m)
    ag.y += uniform(-m, m)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    # detecting collision and simulating death or birth
    neighbors = [nb for nb in agents if nb.type != ag.type
                 and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]

    if ag.type == 'r':
        if len(neighbors) > 0: # if there are foxes nearby
            if random() < dr:
                agents.remove(ag)
                return
        if random() < rr*(1-sum([1 for x in agents if x.type == 'r'])/nr):
            agents.append(cp.copy(ag))
    else:
        if len(neighbors) == 0: # if there are no rabbits nearby
            if random() < df:
                agents.remove(ag)
                return
        else: # if there are rabbits nearby
            if random() < rf:
                agents.append(cp.copy(ag))

def update():
    global agents, rdata, fdata
    t = 0.
    while t < 1. and len(agents) > 0:
        t += 1. / len(agents)
        update_one_agent()

    rdata.append(sum([1 for x in agents if x.type == 'r']))
    fdata.append(sum([1 for x in agents if x.type == 'f']))
    if fdata[-1] == 0:
        rdata[-1] = nr
        return 0
    else:
        return 1

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
# pycxsimulator.GUI().start(func=[initialize, observe, update])


for i_para in range(len(nr_list)):
    print('Parameter number: ' + str(i_para))
    nr = nr_list[i_para]
    r_final = np.zeros(numsims)
    f_final = np.zeros(numsims)

    for i_sim in range(numsims):
        print('    Simulation number: ' + str(i_sim))
        initialize()
        for j in range(N):
            if  j%100 == 0:
                print('      Step ' + str(j))
            if iscontinue == 1:
                iscontinue = update()
            else:
                break

        # r_final[i_sim] = rdata[-1]
        # f_final[i_sim] = fdata[-1]
        r_final[i_sim] = mean(rdata[-50:-1])
        f_final[i_sim] = mean(fdata[-50:-1])

    r_final_avg[i_para] = np.mean(r_final)
    f_final_avg[i_para] = np.mean(f_final)


plt.figure()
plt.plot(nr_list, r_final_avg, color = 'b', marker ='x', markersize = 8, label = 'Rabbit')
plt.plot(nr_list, f_final_avg, color = 'r', marker ='x', markersize = 8, label = 'Fox')

plt.xlabel("Carrying capacity of rabbit population", fontsize = 15)
plt.ylabel("Final number of animals", fontsize = 15)
plt.legend(fontsize = 12)

plt.show(block=True)


