import pymongo
import json
import operator
import pandas as pd

def leggtil():

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Geodata"]
    mycol = mydb["d25-test"]
  
    with open('txtfiler/21.json') as json_file:
            data=json.load(json_file)

    cu=list(mydb.d25.find().limit(1).sort([("_id",pymongo.DESCENDING)]))
    
    
    teller=cu[0]["_id"]+1
    #teller=0
    for i in range(0,len(data['x'])):
             if data['x'][i]>6537600 and data['x'][i]<6537800 and data['y'][i]>305800 and data['y'][i]<306000:
              x = mycol.insert({"_id":teller,"x":data['x'][i],"y":data['y'][i],"z":data['z'][i]})
              print(teller)
              teller+=1


    
    

    #print list of the _id values of the inserted documents:

def Sjekkliste():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Geodata"]
    mycol = mydb["test"]
    cursor=list(mydb.test.aggregate([
        {"$group":{ "_id":{"xcoord": "$xcoord","ycoord":"$ycoord"}}}]))
    print(len(cursor["_id"][1]))
    x = mycol.insert_many(cursor)
    print(cursor)
    #response=[]
    #for doc in cursor:
     #   del doc["dups"][0]
      #  for id in doc["unique_ids"]:
       #     response.append(id)


    #mydb.test.remove({"id":{"$in":response}})

def nosqlsøk():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Geodata"]
    mycol = mydb["test"]
    cu=list(mydb.hundreogeleve.find().limit(1).sort([("_id",pymongo.DESCENDING)]))
    Tall=cu[0]["_id"]
    liste=[]
    nyliste={}
    nyliste['x']=[]
    nyliste['y']=[]
    nyliste['z']=[]
    for i in range(0,Tall,100000):
        liste.append(list(mydb.hundreogeleve.find({"_id":i})))
            
    
    for x in range(0,len(liste)) :
       nyliste['z'].append(liste[x][0]["z"])
       nyliste['x'].append(liste[x][0]["x"])
       nyliste['y'].append(liste[x][0]["y"])
    print(nyliste)
def asctojson():
    fil16=pd.read_fwf("txtfiler/haloen2.asc",header=None)
    x=fil16[0]
    y=fil16[1]
    z=fil16[2]
    coords={}
    coords['x']=[]
    coords['y']=[]
    coords['z']=[]


    for i in range(x.__len__()):
       
            coords['x'].append(x[i])
            coords['y'].append(y[i])
            coords['z'].append(z[i])
    with open('txtfiler/haloen2.json','w')as outfile:
        json.dump(coords,outfile)

def test():

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Geodata"]
    mycol = mydb["d25-test"]
  
    with open('txtfiler/21.json') as json_file:
            data=json.load(json_file)

   # cu=list(mydb.d25-test.find().limit(1).sort([("_id",pymongo.DESCENDING)]))
    
    nyliste= {}
    nyliste['x']=[]
    nyliste['y']=[]
    nyliste['z']=[]
    teller=0
    #teller=0
    for i in range(0,len(data['x'])):
             if data['x'][i]>6537600 and data['x'][i]<6537800 and data['y'][i]>305800 and data['y'][i]<306000:
              nyliste['x'].append(data['x'][i])
              nyliste['y'].append(data['y'][i])
              nyliste['z'].append(data['z'][i])

test()