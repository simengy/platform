import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interp

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from sklearn import cross_validation
from sklearn.metrics import roc_curve, auc
from sklearn.feature_extraction import DictVectorizer

from ..monitor import fetch
from ..threshold import threshold

PLOT_DIR = './plot'


def classifier(metric_name, **kwargs):

    metric1, colnames = fetch(metric_name)
    
    for key in metric1:
        
        train = pd.DataFrame.from_records(metric1[key], columns=colnames)

    
    # Some simple feture engineering
    train_label = train['Fraud']
    
    train = train.drop(['Blind_Submodel',
        'Blind_Model',
        'Household_ID', 'Row_ID', 'Vehicle',
        'Fraud', 'Claim_Amount',
        'pivot_key', 
        #'modularity',
        'betweenness',
        #'pagerank', 
        'community_id'], axis = 1)
    vectorizer = DictVectorizer(sparse = False)
    train_new = vectorizer.fit_transform(train.T.to_dict().values())
    
    
    print train.shape
    print train_new.shape
    feature_name = vectorizer.feature_names_
    print len(feature_name)
    
    # feature selection
    topN = 100
    tree = RandomForestClassifier(200, max_depth=15, n_jobs = -1)
    #indices = feature_selection(tree, train_new, train_label, 
    #        feature_name, topN)
    #train_new = train_new[:, indices] 
    #for i in indices:
    #    print feature_name[i]
   

    forest_2 = LogisticRegression(C=1500, tol=1e-10)
    forest = DecisionTreeClassifier(max_depth=12, min_samples_leaf=1000, max_features=25)
    #forest_2 = RandomForestClassifier(100, n_jobs = 16, max_depth=15)
    #scores = cross_validation.cross_val_score(forest, train_new,
    #        train_label, cv=3, scoring='roc_auc')
    cross_val_curve(train_new, train_label, metric_name, 
            n_folds=5, Base=forest, Link_Analysis=forest_2)
    #print scores


def feature_selection(model, train, label, feature_name, topN = 20):

    model.fit(train, label)
    importances = model.feature_importances_

    indices = np.argsort(importances)[::-1]   
    
    for f in range(topN):
        print ('%d feature %s (%.8f)' % (f+1, feature_name[indices[f]], 
                importances[indices[f]]))

    return indices[:topN]


def cross_val_curve(train, label, metric_name, n_folds=5, **kwargs):
    
    #cv = cross_validation.StratifiedKFold(label, n_folds=n_folds)
    cv = cross_validation.KFold(label.shape[0], n_folds=n_folds, shuffle=True)
   
    # Create dir
    if not os.path.exists('{}/{}'.format(PLOT_DIR, metric_name)):
        os.makedirs('{}/{}'.format(PLOT_DIR, metric_name))
    
    
    for name, model in kwargs.iteritems():

        mean_tpr = 0.0
        mean_fpr = np.linspace(0, 1, 200)

        for i, (ind_train, ind_test) in enumerate(cv):
            probas = model.fit(train[ind_train], label[ind_train]).predict_proba(train[ind_test])

            fpr, tpr, thresholds = roc_curve(label[ind_test], probas[:, 1])
            mean_tpr += interp(mean_fpr, fpr, tpr)
            mean_tpr[0] = 0.0

            #roc_auc = auc(fpr, tpr)
            #plt.plot(fpr, tpr, lw=1, label='Link ROC fold %d (auc = %0.2f)'
            #        % (i, roc_auc))

    
        mean_tpr /= len(cv)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
    
        plt.plot(mean_fpr, mean_tpr, lw=1, label='%s ROC (auc = %0.2f)'
                % (name, mean_auc))

    
    plt.plot([0,1], [0,1], '--', color=(0.6, 0.6, 0.6), label='Random Model')
    
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc='lower right')

    plt.savefig('{}/{}/roc_curve.png'.format(PLOT_DIR, metric_name))



if __name__ == '__main__':
    
    classifier('insurance fraud')
