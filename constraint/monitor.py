from ..connection import connection
from ..metric import datatype


def find_dtype(metric_id):

    query = '''
    SELECT value from
    parameter.METRIC_CONFIG
    where METRIC_ID = {}
    and parameter = 'datatype'
    '''.format(metric_id)

    try:
        dtype, _ = connection.connect(query)
        return dtype[0][0]
    except Exception, err:
        print err
        message = err[1].replace('\'', '\'\'')
        print message
        error_log = '''
        UPDATE parameter.METRIC
        set STATUS = 'ERROR: {}'
        WHERE METRIC_ID = {}
        '''.format(message, metric_id)
        
        connection.connect(error_log)
        
        return None

def get_description(metric_name):

    query = '''
    SELECT * from parameter.METRIC_RESULTS
    WHERE METRIC_ID in
    (
        SELECT METRIC_ID from parameter.METRIC
        WHERE METRIC_NAME = '{}'
    )
    '''.format(metric_name)

    return connection.connect(query)


def fetch(metric_name):
    
    # Getting meta table names
    meta, _ = get_description(metric_name)
    
    if meta is not None:
        dtype = find_dtype(meta[0][0])
    print dtype
    
    data = {}
    columns = []
    for param in meta:

        #print param
        
        query = '''
        SELECT * from metadata.{}
        '''.format(param[4])
        
        # RESULT_ID = 0 only for validation purpose
        if param[4].split('_')[-1] != '0': 
            temp, columns  = connection.connect(query)
            data[param[2]] = datatype.parser[dtype]().cast(temp)

    return data, columns


if __name__ == '__main__':

    print get_description(metric_name = 'age of passenger')
    #dictionary, name = fetch(metric_name = 'Demo TEST')
    dictionary, name = fetch(metric_name = 'age of passenger')
    
    for key in dictionary:
        print '\nKEY\n', key, dictionary[key][0]
