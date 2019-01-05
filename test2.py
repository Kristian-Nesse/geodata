import numpy as np
import matplotlib.mlab as ml
import pandas as pd
import scipy
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits import mplot3d


fil16=pd.read_fwf('storre.txt',header=None)

#Datatype float 64 om til numpy array
x=np.array(fil16[0])
y=np.array(fil16[1])
z=np.array(fil16[2])

xi = np.linspace(min(x), max(x))
yi = np.linspace(min(y), max(y))
X, Y = np.meshgrid(x, y)



points=[]
for i in range(x.__len__()):
	points.append([y[i],x[i]])

Z = griddata(points, z, (X, Y),method='cubic')

print(Z)
print(X)

fig=plt.figure()

ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
ax.set_title('surface');

plt.show()