import os
import pandas as pd
import numpy as np

from sklearn.tree import DescisionTreeClassifier

from ..monitor import fetch
from ..threshold import threshold


def classfier(metric_name, **kwargs):

    metric1, colnames = fetch(metric_name)
    metric = pd.DataFrame(np.array(metric1), columns = colnames)

    print metric1
