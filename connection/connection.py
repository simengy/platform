import pyodbc
import numpy as np

def connect(driver, query):
   #cnxn = pyodbc.connect('DSN=trial')
   cnxn = pyodbc.connect('DRIVER={};\
           SERVER=localhost;DATABASE=test;\
           UID=simengy'.format(driver))
   cursor = cnxn.cursor()
   cursor.execute(query)

   data = cursor.fetchall()
   data = np.array(data)

   return data


if __name__ == '__main__':

    query = 'select * from TITANIC limit 10'

    data = connect('{mySQL}', query)

    print data
