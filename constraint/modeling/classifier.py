import os
import pandas as pd
import numpy as np

from sklearn.tree import DecisionTreeClassifier

from ..monitor import fetch
from ..threshold import threshold


def classifier(metric_name, **kwargs):

    metric1, colnames = fetch(metric_name)
    
    for key in metric1:
        
        metric = pd.DataFrame.from_records(metric1[key], columns=colnames)

    print metric

if __name__ == '__main__':
    
    #classifier('Demo test')
    classifier('age of passenger')

