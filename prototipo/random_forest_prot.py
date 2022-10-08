import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

data = pd.read_csv("./california_housing_train.csv")
data.head()

X = data.drop("median_house_value", axis=1)
Y = data["median_house_value"]

Xtr, Xval, Ytr, Yval = train_test_split(X, Y, test_size=0.5, random_state=0)

arveres = RandomForestRegressor(n_estimators=300, random_state=0, n_jobs=-1) 
arveres.fit(Xtr, Ytr)

p = arveres.predict(Xval)

print(np.sqrt(mean_squared_error(Yval, p)))