from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import json
import math
app = Flask(__name__)


@app.route('/')
def index():
    liste=getlist()

    return render_template("D3.html")



def getlist():
  
    with open('data.json') as json_file:
        data=json.load(json_file)
    return data

@app.route('/zoom',methods=['GET','POST'])
def zoom():
    nyliste={}
    if request.method=='POST':
        xstart=None
        xstart=request.form.get('xcoord')
        xslutt=request.form.get('xcoord1')
        zoom=int(request.form.get('zoom'))
        print(xstart)
        if xstart==None:
            return nyliste
        else:
            
       
        
        
       
            liste=getlist()
            nyliste['x']=[]
            nyliste['y']=[]
            nyliste['z']=[]
            if xstart>xslutt:
             xstart1=liste['xcoord'].index(min(liste['xcoord'], key=lambda x:abs(x-round(float(xstart),2))))
             xslutt1=liste['xcoord'].index(min(liste['xcoord'], key=lambda x:abs(x-round(float(xslutt),2))))
            if xstart<xslutt:
             xstart1=liste['xcoord'].index(min(liste['xcoord'], key=lambda x:abs(x-round(float(xslutt),2))))
             xslutt1=liste['xcoord'].index(min(liste['xcoord'], key=lambda x:abs(x-round(float(xstart),2))))
            print(xstart)
             
    
            for i in range(int(xstart1),int(xslutt1)):
          
                if i % zoom== 0 :
                    nyliste['z'].append(liste['zcoord'][i])
                    nyliste['x'].append(liste['xcoord'][i])
                    nyliste['y'].append(liste['ycoord'][i])
        
 
    return jsonify(nyliste)
@app.route('/firstzoom',methods=['GET','POST'])
def firstzoom():
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


    

