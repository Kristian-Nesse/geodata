import scipy as sp
import scipy.interpolate
import pandas as pd
import numpy as np
from matplotlib import cm
import json




fil16=pd.read_fwf('txtfiler/16.asc',header=None)

x=fil16[0]
y=fil16[1]
z=fil16[2]

ex=[]
ey=[]
ez=[]
data = {}
data['xcoord']=[]
data['ycoord']=[]
data['zcoord']=[]

for i in range(x.__len__()):
    if i % 4== 0 :
        data['xcoord'].append(x[i])
        data['ycoord'].append(y[i])
        data['zcoord'].append(z[i])

print(ex.__len__())

with open('data.json','w') as outfile:
    json.dump(data,outfile,indent=2)



