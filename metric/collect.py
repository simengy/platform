from datetime import datetime, timedelta
from random import randrange

from ..connection import connection
from metadata import metadata
import datatype

N = 1000000


def load(metric_id):
    
    query = '''
    SELECT METRIC_NAME, STARTDATE, ENDDATE, PERIOD_IN_SECOND from parameter.METRIC 
    where METRIC_ID = {};'''.format(metric_id)

    parameter, _ = connection.connect(query)

    return parameter[0]
    
def collect(metric_id):
    
    query = '''
    select value from parameter.METRIC_CONFIG
    where METRIC_ID = {} and parameter = 'query';
    '''.format(metric_id)

    try:
        sql,_ = connection.connect(query)
        return sql[0][0]
    
    except Exception, err:
        print err
        error_log = '''
        UPDATE parameter.METRIC
        set STATUS = 'ERROR: {}'
        WHERE METRIC_ID = {}
        '''.format(err, metric_id)
        connection.connect(error_log)
        
        return None

def max_resultID(metric_id):

    query = '''
    SELECT RESULT_ID from
    parameter.METRIC_RESULTS
    where METRIC_ID = {}
    ORDER BY RESULT_ID DESC
    LIMIT 1
    '''.format(metric_id)

    try:
        maxID, _ = connection.connect(query)
        return maxID[0][0]
    except:
        # The first record is supposed from 'READY'
        return -1

# TODO: datatype -- 
def rollingwindows(metric_id, delta=100):
    
    fmt = '%Y-%m-%d %H:%M:%S'

    metric_name, start, end, period  = load(metric_id)
    sql = collect(metric_id)

    if sql is None:
        return False
    
    if start is None or period is None:
        delta = 1
        start = datetime.now()
        end = datetime.now()
        period = 0
    else:
        if end is None:
            end = datetime.now()
 
    if delta == -1:
        delta = (end - start).total_seconds() / period
        res = (end - start).total_seconds() % period
        delta = int(delta)
        
    print 'TIME delta = ', delta, period, end - start

    for i in xrange(delta):
        
        current = start + timedelta(seconds=period)
        
        sql_new = sql.replace(':STARTDATE', 
                "'" + str(datetime.strftime(start, fmt)) + "'" )
        sql_new = sql_new.replace(':ENDDATE',
                "'" + str(datetime.strftime(current, fmt)) + "'" )
        
        print i, datetime.strftime(current, fmt)
        print sql_new
        
        # Dynamically generating result_ID
        result_id = str(max_resultID(metric_id) + 1)
        meta_name = metric_name.replace(' ', '_') + '_' + result_id 

        print result_id, meta_name
        
        create(metric_id, 
                result_id, 
                datetime.strftime(current, fmt),
                meta_name,
                sql_new)

        start = current

    return True


def create(metric_id, result_id, data_datetime, meta_name, sql_new):
    
    query = '''
    INSERT INTO parameter.METRIC_RESULTS 
    (
        METRIC_ID, RESULT_ID, DATA_DATETIME, VALUE
    )
    values
    (
        {}, {}, '{}', '{}'
    );
    '''
    
    # Create computation log
    query = query.format(metric_id, result_id, data_datetime, meta_name)
    try:
        db = connection.connect(query)
    except Exception, err:
        print 'METRIC_ID = ', metric_id
        print 'DATA_DATETIME = ', data_datetime
        print 'ERROR MESSAGE = ', err
    
    # Create metadata for feature engineering
    meta = metadata(metric_id, meta_name, sql_new)
    try:
        meta.dropTable()
        meta.createTable()
    except Exception, err:
        print err
        pass



if __name__ == '__main__':

    metric_id = 6
    print load(metric_id)
    print 'sql:'
    print collect(metric_id)
    print max_resultID(metric_id)

    #rollingwindows(metric_id)
