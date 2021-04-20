import matplotlib.pyplot as plt
import numpy as np


r_final = np.load('final_rabbit.npy')
f_final = np.load('final_fox.npy')
params = np.load('params_set.npy')

nr_list = params[:,0]*(800-200) + 200
dr_list = params[:,1]
df_list = params[:,2]
rf_list = params[:,3]

# plt.figure()
# plt.hist(r_final)
# plt.title('Final rabbit population histogram',fontsize = 14)

# plt.figure()
# plt.hist(f_final)
# plt.title('Final rabbit population histogram',fontsize = 14)


# plt.figure()
# plt.scatter(r_final, f_final)
# plt.xlabel("Final rabbit population", fontsize = 14)
# plt.ylabel("Final fox population", fontsize = 14)
# mtitle = 'Scatter plot of number of fox vs number of rabbit'
# plt.title(mtitle, fontsize = 14)
# plt.show()

# ###### nr scatter plots
# plt.figure()
# plt.scatter(nr_list, r_final)
# plt.xlabel("Carrying capacity of rabit population", fontsize = 14)
# plt.ylabel("Final rabbit population", fontsize = 14)
# mtitle = 'nr vs final rabbit population'
# plt.title(mtitle, fontsize = 14)

# plt.figure()
# plt.scatter(nr_list, f_final)
# plt.xlabel("Carrying capacity of rabit population", fontsize = 14)
# plt.ylabel("Final fox population", fontsize = 14)
# mtitle = 'nr vs final fox population'
# plt.title(mtitle, fontsize = 14)

# plt.show()

# ###### dr scatter plots
# plt.figure()
# plt.scatter(dr_list, r_final)
# plt.xlabel("Death rate of rabbits when it faces foxes", fontsize = 14)
# plt.ylabel("Final rabbit population", fontsize = 14)
# mtitle = 'dr vs final rabbit population'
# plt.title(mtitle, fontsize = 14)


# plt.figure()
# plt.scatter(dr_list, f_final)
# plt.xlabel("Death rate of rabbits when it faces foxes", fontsize = 14)
# plt.ylabel("Final fox population", fontsize = 14)
# mtitle = 'dr vs final fox population'
# plt.title(mtitle, fontsize = 14)

# plt.show()


# ####### df scatter plots
# plt.figure()
# plt.scatter(df_list, r_final)
# plt.xlabel("Death rate of foxes when there is no food", fontsize = 14)
# plt.ylabel("Final rabbit population", fontsize = 14)
# mtitle = 'df vs final rabbit population'
# plt.title(mtitle, fontsize = 14)


# plt.figure()
# plt.scatter(df_list, f_final)
# plt.xlabel("Death rate of foxes when there is no food", fontsize = 14)
# plt.ylabel("Final fox population", fontsize = 14)
# mtitle = 'df vs final fox population'
# plt.title(mtitle, fontsize = 14)

# plt.show()
# ####### df scatter plots
# plt.figure()
# plt.scatter(rf_list, r_final)
# plt.xlabel("Reproduction rate of foxes", fontsize = 14)
# plt.ylabel("Final rabbit population", fontsize = 14)
# mtitle = 'rf vs final rabbit population'
# plt.title(mtitle, fontsize = 14)


# plt.figure()
# plt.scatter(rf_list, f_final)
# plt.xlabel("Reproduction rate of foxes", fontsize = 14)
# plt.ylabel("Final fox population", fontsize = 14)
# mtitle = 'rf vs final fox population'
# plt.title(mtitle, fontsize = 14)


# plt.show()
##### heatmap
fig, ax = plt.subplots()
ax.tricontour(nr_list, df_list, r_final)
cntr2 = ax.tricontourf(nr_list, df_list, r_final)
fig.colorbar(cntr2, ax=ax)
ax.plot(nr_list, df_list, 'ko', ms=3)
# ax.set(xlim=(-2, 2), ylim=(-2, 2))
ax.set_title('Final rabbit population heatmap', fontsize = 14)
plt.xlabel("Carrying capacity of rabbit population", fontsize = 12)
plt.ylabel("Death rate of fox when there is no food", fontsize = 12)

# fig, ax = plt.subplots()
# ax.tricontour(dr_list, rf_list, r_final)
# cntr2 = ax.tricontourf(dr_list, rf_list, r_final)
# fig.colorbar(cntr2, ax=ax)
# ax.plot(dr_list, rf_list, 'ko', ms=3)
# # ax.set(xlim=(-2, 2), ylim=(-2, 2))
# ax.set_title('Final rabbit population heatmap', fontsize = 14)
# plt.xlabel("Death rate of rabbits when it faces foxes", fontsize = 12)
# plt.ylabel("Reproduction rate of foxes", fontsize = 12)


fig, ax = plt.subplots()
ax.tricontour(dr_list, df_list, r_final)
cntr2 = ax.tricontourf(dr_list, df_list, r_final)
fig.colorbar(cntr2, ax=ax)
ax.plot(dr_list, df_list, 'ko', ms=3)
# ax.set(xlim=(-2, 2), ylim=(-2, 2))
ax.set_title('Final rabbit population heatmap', fontsize = 14)
plt.xlabel("Death rate of rabbits when it faces foxes", fontsize = 12)
plt.ylabel("Death rate of foxes when there is no food", fontsize = 12)


fig, ax = plt.subplots()
ax.tricontour(nr_list, df_list, r_final)
cntr2 = ax.tricontourf(nr_list, df_list, f_final)
fig.colorbar(cntr2, ax=ax)
ax.plot(nr_list, df_list, 'ko', ms=3)
# ax.set(xlim=(-2, 2), ylim=(-2, 2))
ax.set_title('Final fox population heatmap', fontsize = 14)
plt.xlabel("Carrying capacity of rabbit population", fontsize = 12)
plt.ylabel("Death rate of fox when there is no food", fontsize = 12)

# fig, ax = plt.subplots()
# ax.tricontour(dr_list, rf_list, r_final)
# cntr2 = ax.tricontourf(dr_list, rf_list, f_final)
# fig.colorbar(cntr2, ax=ax)
# ax.plot(dr_list, rf_list, 'ko', ms=3)
# # ax.set(xlim=(-2, 2), ylim=(-2, 2))
# ax.set_title('Final fox population heatmap', fontsize = 14)
# plt.xlabel("Death rate of rabbits when it faces foxes", fontsize = 12)
# plt.ylabel("Reproduction rate of foxes", fontsize = 12)


fig, ax = plt.subplots()
ax.tricontour(dr_list, df_list, f_final)
cntr2 = ax.tricontourf(dr_list, df_list, f_final)
fig.colorbar(cntr2, ax=ax)
ax.plot(dr_list, df_list, 'ko', ms=3)
# ax.set(xlim=(-2, 2), ylim=(-2, 2))
ax.set_title('Final fox population heatmap', fontsize = 14)
plt.xlabel("Death rate of rabbits when it faces foxes", fontsize = 12)
plt.ylabel("Death rate of foxes when there is no food", fontsize = 12)

plt.show()
