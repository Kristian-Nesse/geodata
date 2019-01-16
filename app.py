from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import json
import math


import pandas as pd
import scipy as sp
import scipy.interpolate
import numpy as np

app = Flask(__name__)
"""Importerer alle nødvendige pakker """

@app.route('/')
def index():
    return render_template("D3.html")
"""Laster indexsiden som kjører når siden blir lastet """


def getlist():
  
    with open('data.json') as json_file:
        data=json.load(json_file)
    return data
"""Henter listen fra mappen og returner den til funksjonen """
@app.route('/zoom',methods=['GET','POST'])
def zoom():
    nyliste={}
    if request.method=='POST':
        #Sjekker om metoden POST er brukt
        xstart=None
        xstart=request.form.get('xcoord')
        xslutt=request.form.get('xcoord1')
        zoom=int(request.form.get('zoom'))
        print(zoom)
        #Definerer variablene som blir sendt fra html siden
        if xstart==None:
            return nyliste
        #Skal slettes
        else:
            liste=getlist()
            #Henter listen
            nyliste['x']=[]
            nyliste['y']=[]
            nyliste['z']=[]
            if xstart>xslutt:
                #Brukes til å definere indexen til start og sluttpunktet som er oppgitt
             xstart1=liste['xcoord'].index(min(liste['xcoord'], key=lambda x:abs(x-round(float(xstart),2))))
             xslutt1=liste['xcoord'].index(min(liste['xcoord'], key=lambda x:abs(x-round(float(xslutt),2))))
            if xstart<xslutt:
                #Er her i tilfelle zoomen er dratt motsatt vei og det første punket er høyere enn det andre
             xstart1=liste['xcoord'].index(min(liste['xcoord'], key=lambda x:abs(x-round(float(xslutt),2))))
             xslutt1=liste['xcoord'].index(min(liste['xcoord'], key=lambda x:abs(x-round(float(xstart),2))))
           
            for i in range(int(xstart1),int(xslutt1)):
                if i % zoom== 0 :
                    nyliste['z'].append(liste['zcoord'][i])
                    nyliste['x'].append(liste['xcoord'][i])
                    nyliste['y'].append(liste['ycoord'][i])
                    #Finner de nødvendige punktene i listen etter start og slutt verdiene til xstart1
            print(nyliste)
            print(len(nyliste['x']))
    return jsonify(nyliste)
#Returnerer listen i ett json format slik at det er mulig for javascript å lese listen rett
@app.route('/firstzoom',methods=['GET','POST'])
def firstzoom():
    #Blir kjørt første gang contour plotet lastes eller visst du zoomer ut
    nyliste={}
    if request.method=='POST':
        zoom=int(request.form.get('zoom'))
        liste=getlist()
        nyliste['x']=[]
        nyliste['y']=[]
        nyliste['z']=[]
        for i in range(0,len(liste['xcoord'])):
            
            if i % zoom== 0 :
                nyliste['z'].append(liste['zcoord'][i])
                nyliste['x'].append(liste['xcoord'][i])
                nyliste['y'].append(liste['ycoord'][i])
    return jsonify(nyliste)


@app.route('/kart')
def kart():
    #Laster kartet til Sondre
    return render_template("kart2.html")

@app.route('/treD',methods=['GET','POST'])
def treD():
    liste=getlist()
    nyliste={}
    nyliste['x']=[]
    nyliste['y']=[]
    nyliste['z']=[]
    xstart=request.form.get('xcoord')
    xslutt=request.form.get('xcoord1')
    zoom=int(request.form.get('zoom'))

    if xstart>xslutt:
                #Brukes til å definere indexen til start og sluttpunktet som er oppgitt
             xstart1=liste['xcoord'].index(min(liste['xcoord'], key=lambda x:abs(x-round(float(xstart),2))))
             xslutt1=liste['xcoord'].index(min(liste['xcoord'], key=lambda x:abs(x-round(float(xslutt),2))))
    if xstart<xslutt:
                #Er her i tilfelle zoomen er dratt motsatt vei og det første punket er høyere enn det andre
             xstart1=liste['xcoord'].index(min(liste['xcoord'], key=lambda x:abs(x-round(float(xslutt),2))))
             xslutt1=liste['xcoord'].index(min(liste['xcoord'], key=lambda x:abs(x-round(float(xstart),2))))

    print(zoom/5)
    
    for i in range(int(xstart1),int(xslutt1)):
      if i % zoom/5== 0 :
          nyliste['z'].append(liste['zcoord'][i])
          nyliste['x'].append(liste['xcoord'][i])
          nyliste['y'].append(liste['ycoord'][i])
    xmin=min(nyliste['x'])
    xmax=max(nyliste['x'])
    ymin=min(nyliste['y'])
    ymax=max(nyliste['y'])
    xi = np.linspace(xmin, xmax)
    yi = np.linspace(ymin, ymax)
    X, Y = np.meshgrid(xi, yi)
    spline = sp.interpolate.Rbf(nyliste['x'],nyliste['y'],nyliste['z'],function='thin-plate')
    Ze = spline(X,Y)
    Ze2=Ze.tolist()
    return jsonify(Ze2)



