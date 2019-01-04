from harfs import writeTo10x10,lesAscFil_0,singleFile10x10,readAscToList
from harfs import PunktListe

import scipy as sp
import scipy.interpolate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm


#__str__ funksjonen funker ikkje med den andre funksjonen.
# Funker også med '-txt' filer

pL = PunktListe('16.asc')  # oppretter liste med innhold fra filnavn fn



print(pL.text())
print(pL.eightProp())

t=readAscToList('16.asc')
print(t.__str__())

