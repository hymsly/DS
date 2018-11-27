# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 15:54:40 2018

@author: himan
"""

#CONSTRUCCION DEL BOSQUE ALEATORIO
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv('tcFiltrada.txt',sep=',')

print(data.head())

columns = data.columns.values.tolist()

predictors = columns[:-1]
target = columns[-1]

X = data[predictors]
Y = data[target]

forest = RandomForestClassifier(n_jobs=2,oob_score=True, n_estimators=5000)

forest.fit(X,Y)

print(forest.oob_decision_function_)

print(forest.oob_score_)