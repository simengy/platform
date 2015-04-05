import pandas as pd
import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

import monitor


def temporal(metric_name):

    metric1, colnames = monitor.fetch(metric_name)
    metric1 = pd.DataFrame(np.array(metric1), columns = colnames)
    
    print metric1

    r = robjects.r
    forecast = importr('forecast')
    grdevices = importr('grDevices')

    data = robjects.FloatVector(metric1['VALUE'].dropna())
    order = robjects.IntVector((0,1,1))
    seasonal = robjects.ListVector({'order': robjects.IntVector((0,1,0)),
        'period': 7})

    fit = r.arima(data, order=order, seasonal=seasonal)
    pred = forecast.forecast(fit, h = 10)

    grdevices.jpeg(file='test.jpg', width=800, height=600)
    r.plot(pred)
    grdevices.dev_off()
    
    print fit




if __name__ == '__main__':

    temporal(metric_name = 'donation')
