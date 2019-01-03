from hafrs import lesAscFil_0
import numpy as np
import pandas as pd

file=pd.read_fwf('16.asc', header=None)


x=np.array(file[0])
y=file[1]
z=file[2]


ex=[]
ey=[]
ez=[]


for i in range(x.__len__()):
    ex.append(x[i])
    ey.append(y[i])
    ez.append(z[i])
    



print(ex)






 

