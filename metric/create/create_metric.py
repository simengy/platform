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
        except Exception, err:
            print err
            return False

        # Drop metatable
        query = '''
            SELECT value FROM parameter.METRIC_RESULTS
            WHERE METRIC_ID = {}
        '''.format(self.metric_id)
        
        try:
            meta_name, _ = connection.connect(query)
        except Exception, err:
            print err
            return False
        
        for table in meta_name:
            print table

            query = '''DROP TABLE metadata.{};
            '''.format(table[0])
            
            try:
                connection.connect(query)
            except Exception, err:
                print err
                pass
                #return False


        query = '''
        DELETE FROM parameter.METRIC_RESULTS
        WHERE METRIC_ID = {}
        '''.format(self.metric_id)
        
        try:
            print query
            connection.connect(query)
        except Exception, err:
            print err
            return False

        return True


if __name__ == '__main__':

    METRIC_ID = 3
    METRIC_NAME = 'age of passenger'
    METRIC_DESCRIPTION = 'test for categorical features'
    STARTDATE = None
    ENDDATE = None
    PERIOD = '86400'

    parameters = ['datatype', 'query']
    values = ['keyvalue', '''SELECT *
    FROM test.TITANIC
            ''']

    
    METRIC_ID = 6
    METRIC_NAME = 'Demo test'
    METRIC_DESCRIPTION = 'test'
    STARTDATE = '2011-01-03'
    ENDDATE = '2011-02-03'
    PERIOD = '86400'
    

    parameters = ['datatype', 'query']
    values = ['scalar', '''SELECT COUNT(distinct projectid)
    FROM test.DONATION
    where donation_timestamp >= :STARTDATE
    and donation_timestamp < :ENDDATE
            ''']
    

#    METRIC_ID = 7
#    METRIC_NAME = 'insurance fraud'
#    METRIC_DESCRIPTION = 'insurance fraud data'
#    STARTDATE = None
#    ENDDATE = None
#    PERIOD = 10000
#
#    parameters = ['datatype', 'query']
#    values = ['keyvalue', '''SELECT *,
#    CASE
#        WHEN Claim_Amount > 0 THEN 1
#        ELSE 0 END Fraud
#    FROM test.INSURANCE
#            ''']


    cr = creation(METRIC_ID)
    cr.remove_metric()

    cr.create_metric(METRIC_NAME, METRIC_DESCRIPTION, STARTDATE,
            ENDDATE, PERIOD)
    
    for i in range(len(parameters)):
        cr.create_config(parameters[i], values[i])

