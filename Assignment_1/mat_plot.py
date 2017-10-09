import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1)

x = np.arange(0,3*np.pi,0.1)
y = np.cos(x)

ax.plot(x, y)
plt.show()

2+2