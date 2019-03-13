from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import json
import math
import random
from scipy.interpolate import griddata
import pymongo
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import time
from flask import Markup
import pandas as pd
import scipy as sp
import scipy.interpolate
import numpy as np

import numpy as np
from scipy.interpolate import RegularGridInterpolator

app = Flask(__name__)
"""Importerer alle nødvendige pakker """

@app.route('/')
def index():
 
    return render_template("kartK.html")

@app.route('/plot',methods=['GET','POST'])
def plot():
    id=request.args.get('id')
    print(id)
    return render_template('plot.html',id=id)
#Første gang plotet blir lastet blir denne lastet
@app.route('/firstzoom',methods=['GET','POST'])
def firstzoom():
    id=list(request.form.get('id'))
    jscoords={}
    jscoords['x']=[]
    jscoords['y']=[]
    jscoords['z']=[]
    ruter=rutenett()
    xstart=[]
    xslutt=[]
    ystart=[]
    yslutt=[]
    test=[]
    midlertidig=""
    for f in range(0,len(id)):
        if id[f]==",":
            
            test.append(midlertidig)
            midlertidig=""
          
        else:
            midlertidig+=id[f]
    test.append(midlertidig)
    
    for s in test:
        
        rute=ruter[float(s)]
        xstart.append(rute[3])
        xslutt.append(rute[2])
        ystart.append(rute[1])
        yslutt.append(rute[0])
    

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Geodata"]
        mycol = mydb["d"+str(s)+"z0"]
        coordinater=[]
        coordinater=list(mycol.find().sort([("x",pymongo.ASCENDING)]))
        for i in range(len(coordinater)):
            jscoords['x'].append(coordinater[i]['y'])
            jscoords['y'].append(coordinater[i]['x'])
            jscoords['z'].append(coordinater[i]['z'])
    print(xstart)
    print(xslutt)
    print(ystart)
    print(yslutt)    
    xmin=min(xslutt)
    xmax=max(xstart)
    ymin=min(yslutt)
    ymax=max(ystart)
    print(xmin)
    print(xmax)
    print(ymin)
    print(ymax)
    xi = np.linspace(xmin, xmax,200)
    yi = np.linspace(ymin, ymax,200)
    triang=tri.Triangulation(jscoords['x'],jscoords['y'])
    interpolator=tri.LinearTriInterpolator(triang,jscoords['z'])
    X, Y = np.meshgrid(xi, yi)
    zi=interpolator(X,Y)
    intcoords={}
    intcoords['x']=xi.tolist()
    intcoords['y']=yi.tolist()
    intcoords['z']=zi.tolist()
    intcoords['xstart']=xmin
    intcoords['xslutt']=xmax
    intcoords['ystart']=ymax
    intcoords['yslutt']=ymin
    return jsonify(intcoords)
@app.route('/zoom',methods=['GET','POST'])
def zoom():
    start_time = time.time()
    id=list(request.form.get('id'))
    sor=float(request.form.get('sor'))
    nord=float(request.form.get('nord'))
    ost=float(request.form.get('ost'))
    vest=float(request.form.get('vest'))
    startx=float(request.form.get('xstart'))
    sluttx=float(request.form.get('xslutt'))
    starty=float(request.form.get('ystart'))
    slutty=float(request.form.get('yslutt'))
    zoomlvl=float(request.form.get('zoom'))/10
    print(startx)
    print(sluttx)
    print(starty)
    print(slutty)
    print(str(round(zoomlvl)))
    jscoords={}
    jscoords['x']=[]
    jscoords['y']=[]
    jscoords['z']=[]
    ruter=rutenett()
    xstart=[]
    xslutt=[]
    ystart=[]
    yslutt=[]
    test=[]
    midlertidig=""
    for f in range(0,len(id)):
        if id[f]==",":
            
            test.append(midlertidig)
            midlertidig=""
          
        else:
            midlertidig+=id[f]
    test.append(midlertidig)
    
    for s in test:
        
        rute=ruter[float(s)]

    

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Geodata"]
        mycol = mydb["d"+str(s)+"z"+str(round(zoomlvl))]
        coordinater=[]
        

        
        xstart1=list(mycol.find({"x":{"$gt":slutty+sor,"$lt":starty-nord},"y":{"$lt":sluttx-ost,"$gt":startx+vest}}).limit(1).sort([("x",pymongo.DESCENDING)]))
        if not xstart1:
            print("tom")
        else:
            ystart.append(xstart1[0]['x'])
        xslutt1=list(mycol.find({"x":{"$gt":slutty+sor,"$lt":starty-nord},"y":{"$lt":sluttx-ost,"$gt":startx+vest}}).limit(1).sort([("x",pymongo.ASCENDING)]))
        if not xslutt1:
            print("tom")
        else:
            yslutt.append(xslutt1[0]['x'])
        ystart1=list(mycol.find({"x":{"$gt":slutty+sor,"$lt":starty-nord},"y":{"$lt":sluttx-ost,"$gt":startx+vest}}).limit(1).sort([("y",pymongo.ASCENDING)]))
        if not ystart1:
            print("tom")
        else:
            xstart.append(ystart1[0]['y'])
        yslutt1=list(mycol.find({"x":{"$gt":slutty+sor,"$lt":starty-nord},"y":{"$lt":sluttx-ost,"$gt":startx+vest}}).limit(1).sort([("y",pymongo.DESCENDING)]))
        if not yslutt1:
            print("tom")
        else:
            xslutt.append(yslutt1[0]['y'])
        coordinater=list(mycol.find({"x":{"$gt":slutty+sor,"$lt":starty-nord},"y":{"$lt":sluttx-ost,"$gt":startx+vest}}).sort([("x",pymongo.ASCENDING)]))

        for i in range(len(coordinater)):
                jscoords['x'].append(coordinater[i]['y'])
                jscoords['y'].append(coordinater[i]['x'])
                jscoords['z'].append(coordinater[i]['z'])
    
    if ost==0 and vest==0:
            xmin=rute[3]
            xmax=rute[2]
            ymin=rute[1]
            ymax=rute[0]
    else:  
            xmin=min(xstart)
            xmax=max(xslutt)
            ymin=min(yslutt)
            ymax=max(ystart)
    print(xstart)
    print(xslutt)
    print(ystart)
    print(yslutt)
    print(xmin)
    print(xmax)
    print(ymin)
    print(ymax)
    print(zoom)
    
    xi = np.linspace(xmin, xmax,200)
    yi = np.linspace(ymin, ymax,200)
    triang=tri.Triangulation(jscoords['x'],jscoords['y'])
    interpolator=tri.LinearTriInterpolator(triang,jscoords['z'])
    X, Y = np.meshgrid(xi, yi)
    zi=interpolator(X,Y)
    #zi=griddata((nyliste['x'],nyliste['y']),nyliste['z'],(xi[None,:],yi[None,:]),method='cubic')
    intcoords={}
    intcoords['x']=xi.tolist()
    intcoords['y']=yi.tolist()
    intcoords['z']=zi.tolist()
    intcoords['xstart']=xmin
    intcoords['xslutt']=xmax
    intcoords['ystart']=ymax
    intcoords['yslutt']=ymin
    print("--- %s seconds ---" % (time.time() - start_time))
    return jsonify(intcoords)

@app.route('/treD',methods=['GET','POST'])
def treD():
    start_time = time.time()
    zoom=int(request.form.get('zoom'))
    zoomlvl=int(int(zoom)/10)
    nord=round(float(request.form.get('nord')),2)
    sor=round(float(request.form.get('sor')),2)
    ost=round(float(request.form.get('ost')),2)
    vest=round(float(request.form.get('vest')),2)
    id=request.form.get('id')
    print(nord)
    print(sor)
    print(ost)
    print(vest)

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Geodata"]
    mycol = mydb["d"+str(id)+"z"+str(zoomlvl)]
    print(zoomlvl)
    print(zoom)
    liste=[]
    nyliste={}
    nyliste['x']=[]
    nyliste['y']=[]
    nyliste['z']=[]
    ruter=rutenett()
    rute=ruter[float(id)]

    xstart=list(mycol.find({"x":{"$gt":rute[0]+sor,"$lt":rute[1]-nord},"y":{"$lt":rute[3]-ost,"$gt":rute[2]+vest}}).limit(1).sort([("x",pymongo.DESCENDING)]))
    xslutt=list(mycol.find({"x":{"$gt":rute[0]+sor,"$lt":rute[1]-nord},"y":{"$lt":rute[3]-ost,"$gt":rute[2]+vest}}).limit(1).sort([("x",pymongo.ASCENDING)]))
    ystart=list(mycol.find({"x":{"$gt":rute[0]+sor,"$lt":rute[1]-nord},"y":{"$lt":rute[3]-ost,"$gt":rute[2]+vest}}).limit(1).sort([("y",pymongo.ASCENDING)]))
    yslutt=list(mycol.find({"x":{"$gt":rute[0]+sor,"$lt":rute[1]-nord},"y":{"$lt":rute[3]-ost,"$gt":rute[2]+vest}}).limit(1).sort([("y",pymongo.DESCENDING)]))
    liste=list(mycol.find({"x":{"$gt":rute[0]+sor,"$lt":rute[1]-nord},"y":{"$lt":rute[3]-ost,"$gt":rute[2]+vest}}).sort([("x",pymongo.ASCENDING)]))

    for i in range(len(liste)):
        nyliste['x'].append(liste[i]['y'])
        nyliste['y'].append(liste[i]['x'])
        nyliste['z'].append(liste[i]['z'])
    xmin=ystart[0]["y"]
    xmax=yslutt[0]["y"]
    ymin=xstart[0]["x"]
    ymax=xslutt[0]["x"]
    xi = np.linspace(xmin, xmax)
    yi = np.linspace(ymin, ymax)
    X, Y = np.meshgrid(xi, yi)
    spline = sp.interpolate.Rbf(nyliste['x'],nyliste['y'],nyliste['z'],function='thin-plate')
    Ze = spline(X,Y)
    Ze2=Ze.tolist()
    return jsonify(Ze2)


def rutenett():
     ruter={1:[6534800,6535000,305600,305800],2:[6535000,6535200,305600,305800],3:[6535200,6535400,305600,305800],4:[6535400,6535600,305600,305800],5:[6535600,6535800,305600,305800],
           6:[6535800,6536000,305600,305800],7:[6536000,6536200,305600,305800],8:[6536200,6536400,305600,305800],9:[6537400,6537600,305600,305800],10:[6534000,6534200,305800,306000],
           11:[6534200,6534400,305800,306000],12:[6534400,6534600,305800,306000],13:[6534600,6534800,305800,306000],14:[6534800,6535000,305800,306000],15:[6534800,6535000,305800,306000],
           16:[6535000,6535200,305800,306000],17:[6535200,6535400,305800,306000],18:[6535400,6535600,305800,306000],19:[6535600,6535800,305800,306000],20:[6535800,6536000,305800,306000],
           21:[6536000,6536200,305800,306000],22:[6536200,6536400,305800,306000],23:[6536400,6536600,305800,306000],24:[6537400,6537600,305800,306000],25:[6537600,6537800,305800,306000],
           26:[6537800,6538000,305800,306000],27:[6538000,6538200,305800,306000],28:[6533600,6533800,306000,306200],29:[6533800,6534000,306000,306200],30:[6534000,6534200,306000,306200],
           31:[6534200,6534400,306000,306200],32:[6534400,6534600,306000,306200],33:[6534600,6534800,306000,306200],34:[6534800,6535000,306000,306200],35:[6535000,6535200,306000,306200],
           36:[6535200,6535400,306000,306200],37:[6535400,6535600,306000,306200],38:[6535600,6535800,306000,306200],39:[6535800,6536000,306000,306200],40:[6536000,6536200,306000,306200],
           41:[6536200,6536400,306000,306200],42:[6536400,6536600,306000,306200],43:[6536600,6536800,306000,306200],44:[6537200,6537400,306000,306200],45:[6537400,6537600,306000,306200],
           46:[6537600,6537800,306000,306200],47:[6537800,6538000,306000,306200],48:[6538000,6538200,306000,306200],49:[6533600,6533800,306200,306400],50:[6533800,6534000,306200,306400],
           51:[6534000,6534200,306200,306400],52:[6534200,6534400,306200,306400],53:[6534400,6534600,306200,306400],54:[6534600,6534800,306200,306400],55:[6534800,6535000,306200,306400],
           56:[6535000,6535200,306200,306400],57:[6535200,6535400,306200,306400],58:[6535400,6535600,306200,306400],59:[6535600,6535800,306200,306400],60:[6535800,6536000,306200,306400],
           61:[6536000,6536200,306200,306400],62:[6536200,6536400,306200,306400],63:[6536400,6536600,306200,306400],64:[6536600,6536800,306200,306400],65:[6536800,6537000,306200,306400],
           66:[6537000,6537200,306200,306400],67:[6537200,6537400,306200,306400],68:[6537400,6537600,306200,306400],69:[6537600,6537800,306200,306400],70:[6537800,6538000,306200,306400],
           71:[6538000,6538200,306200,306400],72:[6533600,6533800,306400,306600],73:[6533800,6534000,306400,306600],74:[6534000,6534200,306400,306600],75:[6534200,6534400,306400,306600],
           76:[6534400,6534600,306400,306600],77:[6534600,6534800,306400,306600],78:[6534800,6535000,306400,306600],79:[6535000,6535200,306400,306600],80:[6535200,6535400,306400,306600],
           81:[6535400,6535600,306400,306600],82:[6535600,6535800,306400,306600],83:[6535800,6536000,306400,306600],84:[6536000,6536200,306400,306600],85:[6536200,6536400,306400,306600],
           86:[6536400,6536600,306400,306600],87:[6536600,6536800,306400,306600],88:[6536800,6537000,306400,306600],89:[6537000,6537200,306400,306600],90:[6537200,6537400,306400,306600],
           91:[6537400,6537600,306400,306600],92:[6537800,6538000,306400,306600],93:[6538000,6538200,306400,306600],94:[6534400,6534600,306600,306800],95:[6534600,6534800,306600,306800],
           96:[6534800,6535000,306600,306800],97:[6535000,6535200,306600,306800],98:[6535200,6535400,306600,306800],99:[6535400,6535600,306600,306800],100:[6535600,6535800,306600,306800],
           101:[6536000,6536200,306600,306800],102:[6536200,6536400,306600,306800],103:[6536400,6536600,306600,306800],104:[6536600,6536800,306600,306800],105:[6536800,6537000,306600,306800],
           106:[6537000,6537200,306600,306800],107:[6537200,6537400,306600,306800],108:[6534600,6534800,306800,307000],109:[6534800,6535000,306800,307000],110:[6535000,6535200,306800,307000],
           111:[6535200,6535400,306800,307000],112:[6535400,6535600,306800,307000],113:[6535600,6535800,306800,307000],114:[6536000,6536200,306800,307000],115:[6536200,6536400,306800,307000],
           116:[6536400,6536600,306800,307000],117:[6536600,6536800,306800,307000],118:[6536800,6537000,306800,307000],119:[6537000,6537200,306800,307000],120:[6537200,6537400,306800,307000],
           121:[6534800,6535000,307000,307200],122:[6535000,6535200,307000,307200],123:[6535200,6535400,307000,307200],124:[6535400,6535600,307000,307200],125:[6535600,6535800,307000,307200],
           126:[6535800,6536000,307000,307200],127:[6536000,6536200,307000,307200],128:[6536200,6536400,307000,307200],129:[6536400,6536600,307000,307200],130:[6536600,6536800,307000,307200],
           131:[6536800,6537000,307000,307200],132:[6537000,6537200,307000,307200],133:[6537200,6537400,307000,307200],134:[6537400,6537600,307000,307200],135:[6535000,6535200,307200,307400],
           136:[6535200,6535400,307200,307400],137:[6535400,6535600,307200,307400],138:[6535600,6535800,307200,307400],139:[6535800,6536000,307200,307400],140:[6536000,6536200,307200,307400],
           141:[6536200,6536400,307200,307400],142:[6536400,6536600,307200,307400],143:[6536600,6536800,307200,307400],144:[6536800,6537000,307200,307400],145:[6537000,6537200,307200,307400],
           146:[6537200,6537400,307200,307400],147:[6537400,6537600,307200,307400],148:[6535000,6535200,307400,307600],149:[6535200,6535400,307400,307600],150:[6535400,6535600,307400,307600],
           151:[6535600,6535800,307400,307600],152:[6535800,6536000,307400,307600],153:[6536000,6536200,307400,307600],154:[6536200,6536400,307400,307600],155:[6536400,6536600,307400,307600],
           156:[6536600,6536800,307400,307600],157:[6536800,6537000,307400,307600],158:[6537000,6537200,307400,307600],159:[6537200,6537400,307400,307600],160:[6537400,6537600,307400,307600],
           161:[6537600,6537800,307400,307600],162:[6534800,6535000,307600,307800],163:[6535000,6535200,307600,307800],164:[6535200,6535400,307600,307800],165:[6535400,6535600,307600,307800],
           166:[6535600,6535800,307600,307800],167:[6535800,6536000,307600,307800],168:[6536000,6536200,307600,307800],169:[6536200,6536400,307600,307800],170:[6536400,6536600,307600,307800],
           171:[6536600,6536800,307600,307800],172:[6536800,6537000,307600,307800],173:[6537000,6537200,307600,307800],174:[6537200,6537400,307600,307800],175:[6537400,6537600,307600,307800],
           176:[6537600,6537800,307600,307800],177:[6537800,6538000,307600,307800],178:[6535200,6535400,307800,308000],179:[6535400,6535600,307800,308000],180:[6535600,6535800,307800,308000],
           181:[6535800,6536000,307800,308000],182:[6536000,6536200,307800,308000],183:[6536200,6536400,307800,308000],184:[6536400,6536600,307800,308000],185:[6536600,6536800,307800,308000],
           186:[6536800,6537000,307800,308000],187:[6537000,6537200,307800,308000],188:[6537200,6537400,307800,308000],189:[6537400,6537600,307800,308000],190:[6537600,6537800,307800,308000],
           191:[6537800,6538000,307800,308000],192:[6538000,6538200,307800,308000],193:[6535800,6536000,308000,308200],194:[6536000,6536200,308000,308200],195:[6536200,6536400,308000,308200],
           196:[6536400,6536600,308000,308200],197:[6536600,6536800,308000,308200],198:[6536800,6537000,308000,308200],199:[6537000,6537200,308000,308200],200:[6537200,6537400,308000,308200],
           201:[6537400,6537600,308000,308200],202:[6537600,6537800,308000,308000],203:[6537800,6538000,308000,308200],204:[6538000,6538200,308000,308200],205:[6536000,6536200,308200,308400],
           206:[6536200,6536400,308200,308400],207:[6536400,6536600,308200,308400],208:[6536600,6536800,308200,308400],209:[6536800,6537000,308200,308400],210:[6537000,6537200,308200,308400],
           211:[6537200,6537400,308200,308400],212:[6537400,6537600,308200,308400],213:[6537600,6537800,308200,308400],214:[6537800,6538000,308200,308400],215:[6538000,6538200,308200,308400],
           216:[6536200,6536400,308400,308600],217:[6536400,6536600,308400,308600],218:[6536600,6536800,308400,308600],219:[6536800,6537000,308400,308600],220:[6537000,6537200,308400,308600],
           221:[6537200,6537400,308400,308600],222:[6537400,6537600,308400,308600],223:[6537600,6537800,308400,308600],224:[6537800,6538000,308400,308600],225:[6538000,6538200,308400,308600],
           226:[6536600,6536800,308600,308800],227:[6536800,6537000,308600,308800],228:[6537000,6537200,308600,308800],229:[6537200,6537400,308600,308800],230:[6537400,6537600,308600,308800],
           231:[6537600,6537800,308600,308800],232:[6537800,6538000,308600,308800],233:[6538000,6538200,308600,308800],234:[6536600,6536800,308800,309000],235:[6536800,6537000,308800,309000],
           236:[6537000,6537200,308800,309000],237:[6537200,6537400,308800,309000],238:[6537400,6537600,308800,309000],239:[6537600,6537800,308800,309000]}
     return(ruter)
