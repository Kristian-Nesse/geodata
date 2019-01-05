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
    if i % 3== 0 :
        ex.append(x[i])
        ey.append(y[i])
        ez.append(z[i])

print(ex.__len__())


xmin=min(ex)
xmax=max(ex)

ymin=min(ey)
ymax=max(ey)


spline = sp.interpolate.Rbf(ex,ey,ez,function='thin-plate')
xi = np.linspace(min(ex), max(ex))
yi = np.linspace(min(ey), max(ey))
X, Y = np.meshgrid(xi, yi)


Z = spline(X,Y)



print(Z)

#plotte i 3d 

fig = plt.figure()

#plot 2d
#plt.contour(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,linewidth=1, antialiased=False);
#ax = plt.axes(projection='3d')
#ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,linewidth=1, antialiased=False)

plt.contour(X, Y, Z, 50, linewidths = 0, colors = 'k',antialiased=False)
plt.pcolormesh(X, Y, Z, cmap = plt.get_cmap('rainbow'))

plt.colorbar() 
#plt.scatter(x, y, marker = 'o', c = 'b', s = 10, zorder = 10)
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)






plt.show()

