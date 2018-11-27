# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 15:54:40 2018

@author: himan
"""

#CONSTRUCCION DEL ARBOL DE DECISION
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import KFold
from sklearn.cross_validation import cross_val_score

data = pd.read_csv('tcFiltrada.txt',sep=',')

#print(data.head())

columns = data.columns.values.tolist()

predictors = columns[:-1]
target = columns[-1]

X = data[predictors]
Y = data[target]

from sklearn.tree import export_graphviz
from graphviz import Source


def graph(ruta,tree):
    with open(ruta,"w") as dotfile:
        export_graphviz(tree,out_file=dotfile,feature_names=predictors)
        dotfile.close()
    file = open(ruta,"r")
    text = file.read()
    print(text)


def getScore(depth,pred,targ):
    tree = DecisionTreeClassifier(criterion="entropy",min_samples_split=20,random_state=99,max_depth=depth)
    tree.fit(pred,targ)
    cv = KFold(n=pred.shape[0],n_folds=500,shuffle=True,random_state=1)
    scores = cross_val_score(tree,pred,targ,scoring="accuracy",cv = cv,n_jobs=1)
    score = np.mean(scores)
    graph("bcp_tree.dot",tree)
    return score

print("Score depth=",8," -> ",getScore(8,X,Y))
