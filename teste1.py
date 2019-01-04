import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits import axes_grid1
import matplotlib.mlab as ml
from scipy.interpolate import griddata
import numpy as np



fil16=pd.read_fwf('storre.txt',header=None)

x=np.array(fil16[0])
y=np.array(fil16[1])
z=np.array(fil16[2])

xi = np.linspace(min(x), max(x))
yi = np.linspace(min(y), max(y))
X, Y = np.meshgrid(xi, yi)




fig=plt.figure()
ax = plt.axes(projection='3d')

ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
ax.set_title('surface');

plt.show()




