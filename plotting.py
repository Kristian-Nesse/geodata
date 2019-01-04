import scipy as sp
import scipy.interpolate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm

fil16=pd.read_fwf('16.asc',header=None)

x=fil16[0]
y=fil16[1]
z=fil16[2]

ex=[]
ey=[]
ez=[]


for i in range(x.__len__()):
    if i % 2== 0 :
        ex.append(x[i])
        ey.append(y[i])
        ez.append(z[i])

print(ex.__len__())




spline = sp.interpolate.Rbf(ex,ey,ez,function='thin-plate')
xi = np.linspace(min(ex), max(ex))
yi = np.linspace(min(ey), max(ey))
X, Y = np.meshgrid(xi, yi)


Z = spline(X,Y)



print(Z)



fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,linewidth=1, antialiased=False)
plt.show()

