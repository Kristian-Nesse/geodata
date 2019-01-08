import json
from hafrs import readAscToList 
from hafrs import PunktListe
from hafrs import PointNED
from KonverterGeo import konvertereFraUTM
from geojson import Polygon,Feature,FeatureCollection,dump

#Må skrive om til rett rekkefølge på koordinatene 

def skrivLonLaTtilJSON(filename,namn):
    J=konvertereFraUTM('16.asc')[0]
    print(J.__len__())
    X=[]
    Y=[]
    for i in range(J.__len__()):
        X.append(J[i][0])
        Y.append(J[i][1])
    xmin=min(X)
    xminIND=X.index(xmin)
    ymin=min(Y)
    yminIND=Y.index(ymin)
    xmax=max(X)
    xmaxIND=X.index(xmax)
    ymax=max(Y)
    ymaxIND=Y.index(ymax)
    print('Minste x-verdi: ' + str(xmin) + ' Index der minste verdi befinner seg: ' + str(xminIND))
    print('Minste y-verdi: ' + str(ymin) + ' Index der minste verdi befinner seg: ' + str(yminIND))
    print('Største x-verdi: ' + str(xmax)+ ' Index der største verdi befinner seg: ' + str(xmaxIND))
    print('Største y-verdi: ' + str(ymax)+ ' Index der største verdi befinner seg: ' + str(ymaxIND))
    #Definerer punkt som trengst til JSON mangekanten
    minX=J[xminIND]
    minY=J[yminIND]
    maxX=J[xmaxIND]
    maxY=J[ymaxIND]
    print(minX)
    print(maxX)
    print(minY)
    print(maxY)
    #Lager liste av desse punkta:
    listeMedPunkt=[minX,maxX,minY,maxY]
    print(listeMedPunkt)
    fila=Polygon(listeMedPunkt)
    features = []
    features.append(Feature(geometry=fila, properties={}))
    # add more features...
    # features.append(...)
    feature_collection = FeatureCollection(features)
    with open('myfile.json', 'w') as f:
        dump(feature_collection, f,indent=2)



   
















