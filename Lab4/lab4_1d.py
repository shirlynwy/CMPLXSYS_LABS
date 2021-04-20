import pycxsimulator
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import copy as cp
from pyDOE import lhs
import numpy.matlib as npm

nsamples = 100
reruns = 2
nparams = 4

# temp = lhs(nparams, samples = nsamples)
# # print(temp)
# params = npm.repmat(lhs(nparams, samples = nsamples),reruns,1) 
# print(params)
# # Set up parameter array

params = npm.repmat(lhs(nparams, samples = nsamples),reruns,1) 
Nparams = np.size(params, 0)
# nr = 500. # carrying capacity of rabbits

r_init = 100 # initial rabbit population
mr = 0.03 # magnitude of movement of rabbits
# dr = 1.0 # death rate of rabbits when it faces foxes
rr = 0.1 # reproduction rate of rabbits

f_init = 30 # initial fox population
mf = 0.05 # magnitude of movement of foxes
# df = 0.1 # death rate of foxes when there is no food
# rf = 0.5 # reproduction rate of foxes

cd = 0.02 # radius for collision detection
cdsq = cd ** 2


# numsims = 6
Nsteps = 400

# nr_list = range(200, 850, 50)
# print(list(nr_list))
# print(nr_list[-1])

r_final= np.zeros(Nparams)
f_final= np.zeros(Nparams)

global nr

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

    # if rdata[-1] == 0:
    #     fdata[-1] = 0
    #     return 0
    if fdata[-1] == 0:
        rdata[-1] = nr
        return 0
    else:
        return 1


# def lighten_color(color, amount=0.5):
#     """
#     Lightens the given color by multiplying (1-luminosity) by the given amount.
#     Input can be matplotlib color string, hex string, or RGB tuple.

#     Examples:
#     >> lighten_color('g', 0.3)
#     >> lighten_color('#F034A3', 0.6)
#     >> lighten_color((.3,.55,.1), 0.5)
#     """
#     import matplotlib.colors as mc
#     import colorsys
#     try:
#         c = mc.cnames[color]
#     except:
#         c = color
#     c = colorsys.rgb_to_hls(*mc.to_rgb(c))
#     return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])
# pycxsimulator.GUI().start(func=[initialize, observe, update])


for i in range(Nparams):
    print('Parameter set number: ' + str(i))
    # print(params[i, :])
    # nr = params[i,0]*(800-200) + 200 # carrying capacity for rabbits
    #                                  # note we have rescaled the 0,1 range of params[i,0] to match the range for nr!
    # dr = params[i,1] # death probability for rabbits when encountering fox
    # df = params[i,2] # death probability for foxes when no food available
    # rf = params[i,3] # reproduction probability for foxes when food available
    # nr = 490.73199933342875
    # dr = 0.6946583745195399
    # df = 0.09994668816475707
    # rf = 0.5142417171564949


    nr = params[i,0]*(800-200) + 200 # carrying capacity for rabbits (200 to 700)
    dr = params[i,1]*0.5+0.5 # death probability for rabbits when encountering fox (0.5 to 1)
    df = params[i,2] # death probability for foxes when no food available (0 to 0.25)
    rf = params[i,3]# reproduction probability for foxes when food available (0.25 to 0.75)
    initialize()
    print('nr = '+ str(nr))
    print('dr = ' + str(dr))
    print('df = ' + str(df))
    print('rf = ' + str(rf))

    for j in range(Nsteps):
        if  j%100 == 0:
                print('    Step' + str(j))

        if iscontinue == 1:
            iscontinue = update()
        else:
            break
        
    r_final[i] = rdata[-1]
    # print('Rabbit:')
    # print(rdata)
    f_final[i] = fdata[-1]
    # print('Fox:')
    # print(fdata)




# hist1 = np.histogram(r_final)

plt.figure()
plt.hist(r_final)
plt.title('Final rabbit population histogram',fontsize = 14)

plt.figure()
plt.hist(f_final)
plt.title('Final rabbit population histogram',fontsize = 14)

plt.figure()
plt.scatter(r_final, f_final)
plt.xlabel("Final rabbit population", fontsize = 14)
plt.ylabel("Final fox population", fontsize = 14)
mtitle = 'Scatter plot of number of fox vs number of rabbit'
plt.title(mtitle, fontsize = 14)

# with open('test.npy', 'params') as f:
#      np.save(f, params)
np.save('params_set.npy', params)
np.save('final_rabbit.npy', r_final)
np.save('final_fox.npy', f_final)

plt.figure()
plt.plot(r_final, color = 'b', marker ='x', markersize = 8, label = 'Rabbit')
plt.plot(f_final, color = 'r', marker ='x', markersize = 8, label = 'Fox')

# plt.xlabel("Carrying capacity of rabbit population", fontsize = 15)
# plt.ylabel("Final number of animals", fontsize = 15)
plt.legend(fontsize = 12)

plt.show(block=True)

# with open('params_set.npy', 'params') as f:
# aa = np.load('params_set.npy')
# print(aa)
# bb = np.load('final_rabbit.npy')
# print(bb)
# cc = np.load('final_fox.npy')
# print(cc)

