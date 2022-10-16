import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import plot_tree

df = pd.read_csv('./tables/TABELA_TCC.csv')

X = df.drop('RISCO',axis=1)
y = df['RISCO']

X_tr, X_ts, y_tr, y_ts = train_test_split(X,y, test_size=0.30, random_state=61658)

rf = RandomForestClassifier(max_depth=22, random_state=61658, n_estimators=10)
rf.fit(X_tr, y_tr)

for x in range(len(rf.estimators_)):
    plt.figure(figsize=(75,20))
    plot_tree(rf.estimators_[x],filled=True)
    plt.savefig(f"./../../Anexos/figura_{x + 1}.jpg")

amostra = [[0,80,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
print(rf.predict(amostra))