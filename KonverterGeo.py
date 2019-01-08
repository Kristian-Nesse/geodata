import pandas as pd
import numpy as np
import utm
import json

#Tenke på og senere konvertere til Json også

def konvertereFraUTM(filename):
    #leser inn fil der xy-koordinater er på UTM32 format
    fil16=pd.read_fwf(filename,header=None)
    x=fil16[0]
    z=np.array(fil16[2])
    xy=fil16.iloc[:,0:2]
    XY=xy.values.tolist()
    #print(x.__len__())
    #print(z.__len__())
    hei=[]
    for i in range(x.__len__()):
        hei.append(utm.to_latlon(XY[i][1],XY[i][0],32,'U'))
    X=[]
    Y=[]
    for i in range(x.__len__()):
        X.append(hei[i][0])
        Y.append(hei[i][1])
    #Konverterer til numpy array
    xx=np.array(X)
    yy=np.array(Y)
    Ferdig=[]
    for i in range(x.__len__()):
        Ferdig.append([xx[i],yy[i],z[i]])

    
    
    
    return hei,Ferdig

#Eksempel

#Konvertere fil til Json

#MERK syntax for å kunn aksessere den første returnerte verdien fra metoden 

#J=konvertereFraUTM('16.asc')[0]
#rint(J)
























