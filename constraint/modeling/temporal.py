import os
import pandas as pd
import pandas.rpy.common as com
import numpy as np
import rpy2.robjects as robjects

from rpy2.robjects.packages import importr

from ..monitor import fetch
from ..threshold import threshold

PLOT_DIR = 'plot'


def temporal(metric_name):

    metric1, colnames = fetch(metric_name)
    metric1 = pd.DataFrame(np.array(metric1), columns = colnames)
    
    print metric1

    # allocate the size of test data
    size = 10
    train = metric1[:-size]
    test = metric1[-size:]

    start = train.shape[0] + 1
    end = train.shape[0] + test.shape[0]
    
    # R wrapper
    r = robjects.r
    forecast = importr('forecast')
    grdevices = importr('grDevices')

    train = robjects.FloatVector(train['VALUE'].dropna())
    test = robjects.FloatVector(test['VALUE'].dropna())
    order = robjects.IntVector((3,1,2))
    seasonal = robjects.ListVector({'order': robjects.IntVector((1,1,1)),
        'period': 7})

    fit = r.arima(train, order=order, seasonal=seasonal)
    pred = forecast.forecast(fit, h=end-start+1)

    # Plotting
    if not os.path.exists('{}/{}'.format(PLOT_DIR, metric_name)):
        os.makedirs('{}/{}'.format(PLOT_DIR, metric_name))

    grdevices.jpeg(file='{}/{}/test.jpg'.format(PLOT_DIR, metric_name),
            width=800, height=600)
    r.plot(pred, xlab='Days', ylab='Donation Amount')
    r.lines(x=r.seq(start,end), y=test, col='red', type='b', lwd=2)
    grdevices.dev_off()
    
    # ZOOM-IN
    grdevices.jpeg(file='{}/{}/test_zoomin.jpg'.format(PLOT_DIR, metric_name),
            width=800, height=600)
    r.plot(pred, xlim=r.range(start,end), xlab='Days', ylab='Donation Amount')
    r.lines(x=r.seq(start,end), y=test, col='red', type='b', lwd=2)
    grdevices.dev_off()

    # Threshold and alerting
    pred = list(pred)
    ci = '80%'
    
    threshold(com.convert_robj(pred[4])[ci].as_matrix(),
            com.convert_robj(pred[5])[ci].as_matrix(),
            com.convert_robj(test),
            metric_name = metric_name,
            image = '{}/{}/test.jpg'.format(PLOT_DIR, metric_name),
            ci_level = ci
            )
    

if __name__ == '__main__':

    #temporal(metric_name = 'donation')
    #temporal(metric_name = 'donation_dup')
    temporal(metric_name = 'donation_project')

