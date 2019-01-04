from hafrs import lesAscFil_0
import numpy as np
import pandas as pd
import pymysql.cursors

file=pd.read_fwf('txtfiler/16.asc', header=None)


x=np.array(file[0])
y=file[1]
z=file[2]


ex=[]
ey=[]
ez=[]




        # Create a new record
        
        
#for i in range(x.__len__()):
 #               connection = pymysql.connect(host='localhost',
  #                           user='root',
   #                          password='root',
    #                         db='kristian',
     #                        charset='utf8mb4',
      #                       cursorclass=pymysql.cursors.DictCursor)
       #         try:
        #            with connection.cursor() as cursor:
         #               sql = "INSERT INTO `coords` (`xcoord`, `ycoord`,`zcoord`) VALUES (%s, %s, %s)"
          #              cursor.execute(sql, (float(x[i]), float(y[i]),float(z[i])))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
                        #connection.commit()
                #finally:
                 #   connection.close()

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='kristian',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
                    with connection.cursor() as cursor:
                        sql = "select * from coords where zcoord = ( select min(zcoord) from coords);"
                        cursor.execute(sql)
                        result = cursor.fetchone()
                        print(result)

    # connection is not autocommit by default. So you must commit to save
    # your changes.
                        connection.commit()
finally:
                    connection.close()
    







 

