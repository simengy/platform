from ..connection import connection 
from throttle import periodicTask
import collect


def inquiry():

    print 'Inquiring database:'

    query = '''
    SELECT * FROM parameter.METRIC
    WHERE STATUS = 'PENDING'
    '''

    pending_list, _ = connection.connect(query)
    
    query = '''
    SELECT * FROM parameter.METRIC
    WHERE STATUS = 'DEPLOYING'
    '''

    deployed_list, _ = connection.connect(query)
    
    return pending_list, deployed_list

def execute():

    pending_list, deployed_list = inquiry()
   
    # Only compute the first elements for sanity check
    print 'PENDING:'
    for pls in pending_list:
        metric_id = pls[0]
        print metric_id
        
        if collect.rollingwindows(metric_id, delta=1):
            # reset status
            query = '''
            UPDATE parameter.METRIC set STATUS = 'READY'
            WHERE METRIC_ID = {}
            '''.format(metric_id)
           
            connection.connect(query)

    # If everything wroks fine, change METRIC status to 'DEPLOYED'
    print 'DEPLOYING:'
    for dls in deployed_list:
        metric_id = dls[0]
        print metric_id
        
        if collect.rollingwindows(metric_id, delta=-1):
            # reset status
            query = '''
            UPDATE parameter.METRIC set STATUS = 'DEPLOYED'
            WHERE METRIC_ID = {}
            '''.format(metric_id)
            
            connection.connect(query)

def run(worker, interval = 10):

    task = periodicTask(interval=interval, callback=execute)
    task.throttle()


if __name__ == '__main__':

    #print inquiry()
    #execute()
    run(inquiry, interval=5)
