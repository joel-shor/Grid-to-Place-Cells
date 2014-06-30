from matplotlib import pyplot as plt
import numpy as np

x = np.array(range(1,68))

def f(x):
    return np.power(1.1,x-67)*(404-60)+60

y = f(x)

plt.plot(x,y)
plt.show()

for i in x:
    print f(i)