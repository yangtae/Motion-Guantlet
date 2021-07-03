import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('sensor.csv', index_col='index')

train, test = train_test_split(df, test_size=0.2)
print(train.head())

rf = RandomForestClassifier()

X = train.drop('target', axis=1)
y= train['target']

rf.fit(X, y)

X_test = test.drop('target', axis=1)
y_test = test['target']

filename = 'finalized_model.sav'
pickle.dump(rf, open(filename, 'wb'))


