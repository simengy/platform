from ...connection import connection

class creation:

    def __init__(self, metric_id):
        
        self.metric_id = metric_id

    def create_metric(self, metric_name, metric_description, 
            startdate, enddate, period):

        query = '''
        INSERT INTO parameter.METRIC
        (
            METRIC_ID, 
            METRIC_NAME,
            METRIC_DESCRIPTION,
            STARTDATE,
            ENDDATE,
            PERIOD_IN_SECOND
        )
        VALUES
        (
            {},'{}','{}','{}','{}',{}
        )
        '''.format(self.metric_id, metric_name, 
                metric_description, startdate, enddate, period)
        
        connection.connect(query)

    def create_config(self, parameter, value):
        
        query = '''
        INSERT INTO parameter.METRIC_CONFIG
        values
        ({},'{}','{}')
        '''.format(self.metric_id, parameter, value)

        connection.connect(query)

    def remove_metric(self):

        query = '''
        DELETE FROM parameter.METRIC
        WHERE METRIC_ID = {}
        '''.format(self.metric_id)

        try:
            connection.connect(query)
        except:
            return False
        
        query = '''
        DELETE FROM parameter.METRIC_CONFIG
        WHERE METRIC_ID = {}
        '''.format(self.metric_id)
        
        try:
            connection.connect(query)
        except:
            return False

        query = '''
        DELETE FROM parameter.METRIC_RESULTS
        WHERE METRIC_ID = {}
        '''.format(self.metric_id)
        
        try:
            connection.connect(query)
        except:
            return False

        return True



if __name__ == '__main__':

    METRIC_ID = 4
    METRIC_NAME = 'age of customer'
    METRIC_DESCRIPTION = 'test only'
    STARTDATE = '2011-03-05'
    ENDDATE = '2012-04-05'
    PERIOD = '144000'

    parameters = ['datatype', 'query']
    values = ['int', '''SELECT COUNT(*)
    FROM test.DONATION
    WHERE donation_timestamp >= :STARTDATE
    AND donation_timestamp < :ENDDATE
            ''']

    cr = creation(METRIC_ID)
    cr.remove_metric()

    cr.create_metric(METRIC_NAME, METRIC_DESCRIPTION, STARTDATE,
            ENDDATE, PERIOD)
    
    for i in range(len(parameters)):
        cr.create_config(parameters[i], values[i])

