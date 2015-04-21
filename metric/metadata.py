from ..connection import connection


class metadata:
    
    def __init__(self, metric_id, tablename, query, source=None):
        
        self.metric_id = metric_id
        self.tablename = tablename
        self.query = query
        self.source = source
        
    def dropTable(self):
        
        drop_sql = '''
        DROP TABLE IF EXISTS metadata.{};
        '''.format(self.tablename)
        
        connection.connect(drop_sql)
            
    def deleteTable(self):
        
        del_sql = '''
        DELETE FROM metadata.{};
        '''.format(self.tablename)
        
        connection.connect(del_sql)

    def createTable(self):

        create_sql = '''
        CREATE TABLE IF NOT EXISTS metadata.{}
        (
            {}
        );
        '''.format(self.tablename, self.query)

        connection.connect(create_sql)

    def importCSV(self):
        
        query = '''
        load data local infile '{}'
        into table metadata.{}
        fields terminated by ','
        enclosed by '\"'
        lines terminated by '\\n'
        ignore 1 lines;
        '''.format(self.source, self.tablename)
        print 'check0',  query 
        
        try:
            connection.connect(query)
        except Exception, err:
            
            message = err[1].replace('\'', '\'\'' )
            print message 
            
            err_query = '''
            UPDATE parameter.METRIC_RESULTS
            set VALUE = '{}'
            WHERE metric_id = {};
            '''.format(message, self.metric_id)
            
            connection.connect(err_query)

    def duplicateData(self):
        # TBD
        return


if __name__ == '__main__':

    sql = '''
    SELECT * FROM test.TITANIC
    '''
    metatable_name = 'TITANIC_meta'

    cr = metadata(3, metatable_name, sql, 'sql/sql_data/TITANIC/titanic.csv')

    cr.dropTable()
    cr.createTable()
    cr.deleteTable()
    cr.importCSV()
