import pyodbc
import numpy as np

def connect(query, driver='{MySQL}'):
    
    #cnxn = pyodbc.connect('DSN=trial')
    cnxn = pyodbc.connect('DRIVER={};\
           SERVER=localhost;DATABASE=test;\
           UID=simengy'.format(driver))
    cursor = cnxn.cursor()
    cursor.execute(query)
    
    try:
        data = cursor.fetchall()
    except:
        data = None

    cnxn.commit()
    cnxn.close()

    return data


if __name__ == '__main__':

    query = 'select * from TITANIC limit 10'

    data = connect(query)
    data = np.array(data)

    print data
