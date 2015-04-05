from ..connection import connection

import pandas as pd


def fetch(metric_name):

    query = '''
    SELECT * from parameter.METRIC_RESULTS
    WHERE METRIC_ID in
    (
        SELECT METRIC_ID from parameter.METRIC
        WHERE METRIC_NAME = '{}'
    )
    '''.format(metric_name)

    return connection.connect(query)


if __name__ == '__main__':

    print fetch(metric_name = 'donation')
