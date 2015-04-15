from datetime import datetime, timedelta
from random import randrange

from ..connection import connection
import datatype
import parser

N = 1000000

def load(metric_id):
    
    query = '''
    SELECT STARTDATE, ENDDATE, PERIOD_IN_SECOND from parameter.METRIC 
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
        error_log = '''
        UPDATE parameter.METRIC
        set STATUS = 'ERROR: {}'
        WHERE METRIC_ID = {}
        '''.format(err, metric_id)
        connection.connect(error_log)
        
        return None
    
# TODO: datatype -- 
def rollingwindows(metric_id, delta=100):
    
    fmt = '%Y-%m-%d %H:%M:%S'

    start, end, period  = load(metric_id)
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


    metric = {}
    for i in xrange(delta):
        
        current = start + timedelta(seconds=period)
        
        sql_new = sql.replace(':STARTDATE', 
                "'" + str(datetime.strftime(start, fmt)) + "'" )
        sql_new = sql_new.replace(':ENDDATE',
                "'" + str(datetime.strftime(current, fmt)) + "'" )
        
        print i, datetime.strftime(current, fmt)
        print sql_new
        
        try:
            metric[current], _ = connection.connect(sql_new)
        except Exception, err:
            err[1].replace('\'', '\'\'' )
            
            error_log = '''
            UPDATE parameter.METRIC
            set STATUS = 'ERROR: {}'
            WHERE METRIC_ID = {}
            '''.format(err, metric_id)
            connection.connect(error_log)
        
            return False
 
        start = current

    for key in sorted(metric):

        dtype = find_dtype(metric_id)
        print 'RESULT:\n', metric[key], dtype
        
        if dtype is None:
            return False
        
        for v in metric[key]:

            value = datatype.parser[dtype]().cast(v)
            create(metric_id, datetime.strftime(key, fmt), value)

    return True


def create(metric_id, data_datetime, value):
    
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
    
    result_id = str(metric_id) + str(randrange(N))

    query = query.format(metric_id, result_id, data_datetime, value)
    
    try:
        db = connection.connect(query)
    
    except Exception, err:
        
        print 'METRIC_ID = ', metric_id
        print 'DATA_DATETIME = ', data_datetime
        print 'ERROR MESSAGE = ', err


if __name__ == '__main__':

    metric_id = 3
    print load(metric_id)
    print 'sql:'
    print collect(metric_id)

    rollingwindows(metric_id)
