from matplotlib import pyplot as plt

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

y1 = range(10)
y1lower = [y-1 for y in y1]
y1upper = [y+1 for y in y1]
ax1.errorbar(range(10),y1,yerr=[y1lower,y1upper],color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')

y2 = [-20]*10
y2lower = [1]*10
y2upper = [1]*10
ax2.errorbar(range(10),y2,yerr=[y2lower,y2upper],color='g')
for tl in ax2.get_yticklabels():
    tl.set_color('g')

plt.show()

