import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import pandas as pd
import scipy as sp
import scipy.interpolate
import numpy as np




# Read data from a csv
z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')


plotly.tools.set_credentials_file(username='SadSuzio', api_key='y7cGhxll5T7aUyObhsdH')



def Interpolering3d(filename):

    fil16=pd.read_fwf(filename,header=None)

    print(fil16)



    x=fil16[0]
    y=fil16[1]
    z=fil16[2]

    ex=[]
    ey=[]
    ez=[]


    for i in range(x.__len__()):
        if i % 20== 0 :
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


    Ze = spline(X,Y)


    sett=pd.DataFrame(Ze)
    #print(Ze)

    return sett

z_data=Interpolering3d('16.asc')


data = [
    go.Surface(
        z=z_data.as_matrix()
    )
]
layout = go.Layout(
    title='Mt Bruno Elevation',
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=65,
        r=50,
        b=65,
        t=90
    )
)
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='plottttt.html')

































data = [
    go.Surface(
        z=sett.as_matrix(),
        contours=go.surface.Contours(
            z=go.surface.contours.Z(
              show=True,
              usecolormap=True,
              highlightcolor="#42f462",
              project=dict(z=True)
            )
        )
    )
]


layout = go.Layout(
    width=800,
    height=700,
    autosize=False,
    title='Fil 16 datasett',
    scene=dict(
        xaxis=dict(
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=True,
            backgroundcolor='rgb(230, 230,230)'
           


        ),
        yaxis=dict(
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=True,
            backgroundcolor='rgb(230, 230,230)'
            

        ),
        zaxis=dict(
            gridcolor='rgb(255, 255, 255)',
            zerolinecolor='rgb(255, 255, 255)',
            showbackground=True,
            backgroundcolor='rgb(230, 230,230)'
        ),
        aspectratio = dict( x=1, y=1, z=0.7 ),
        aspectmode = 'manual'
    )
)



fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='elevations-3d-surface')


