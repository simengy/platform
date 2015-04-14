from datetime import datetime, timedelta
from random import randrange

from ..connection import connection


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

    sql,_ = connection.connect(query)

    return sql[0][0]

def rollingwindows(metric_id, delta=100):

    fmt = '%Y-%m-%d %H:%M:%S'
    
    start, end, period  = load(metric_id)
    sql = collect(metric_id)

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
        
        metric[current], _ = connection.connect(sql_new)
 
        start = current

    for key in sorted(metric):

        print 'RESULT:'
        print metric[key]

        create(metric_id, datetime.strftime(key, fmt), metric[key][0][0])


def create(metric_id, data_datetime, value):
    
    query = '''
    INSERT INTO parameter.METRIC_RESULTS 
    (
        METRIC_ID, RESULT_ID, DATA_DATETIME, VALUE
    )
    values
    (
        {}, {}, '{}', {}
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

    print load(1)
    print 'sql:'
    print collect(1)

    #rollingwindows(1)
