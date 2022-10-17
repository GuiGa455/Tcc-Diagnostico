from logging import exception
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import plot_tree

from data_model import dadosPaciente

import json

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = {}

df = pd.read_csv('./tables/TABELA_TCC.csv')
rf = None

def gerar_arvore():
    X = df.drop('RISCO',axis=1)
    y = df['RISCO']
    global rf

    X_tr, X_ts, y_tr, y_ts = train_test_split(X,y, test_size=0.30, random_state=61658)

    rf = RandomForestClassifier(max_depth=22, random_state=61658, n_estimators=10)
    rf.fit(X_tr, y_tr)

def gerar_img():
    global rf
    if rf is None:
        return 0
    for x in range(len(rf.estimators_)):
        plt.figure(figsize=(75,20))
        plot_tree(rf.estimators_[x],filled=True)
        plt.savefig(f"./../../Anexos/figura_{x + 1}.jpg")
    return 1

def analisar_risco(data = dadosPaciente()):
    amostra = [[
    data.OVA,
    data.DISP,
    data.FR,
    data.CIA,
    data.RAA1,
    data.MVUA,
    data.ROVA,
    data.ER,
    data.CAG,
    data.RAA2,
    data.MVPA1,
    data.HEM,
    data.SAT1,
    data.TPEH,
    data.MVPA2,
    data.TP,
    data.DGSI1,
    data.SAT2,
    data.COR,
    data.DGSI2,
    data.TS,
    data.SG,
    ]]
    global rf
    if rf is None:
        return 0
    data = rf.predict(amostra)
    return int(data[0])

@app.get("/pre_classificacao/read")
def get_pre_classificacao(
    OVA: int = 0,
    DISP: int = 80,
    FR: int = 0,
    CIA: int = 0,
    RAA1: int = 0,
    MVUA: int = 0,
    ROVA: int = 0,
    ER: int = 0,
    CAG: int = 0,
    RAA2: int = 0,
    MVPA1: int = 0,
    HEM: int = 0,
    SAT1: int = 0,
    TPEH: int = 0,
    MVPA2: int = 0,
    TP: int = 0,
    DGSI1: int = 0,
    SAT2: int = 0,
    COR: int = 0,
    DGSI2: int = 0,
    TS: int = 0,
    SG: int = 0,
):
    try:
        data = dadosPaciente(
            OVA=OVA,
            DISP=DISP,
            FR=FR,
            CIA=CIA,
            RAA1=RAA1,
            MVUA=MVUA,
            ROVA=ROVA,
            ER=ER,
            CAG=CAG,
            RAA2=RAA2,
            MVPA1=MVPA1,
            HEM=HEM,
            SAT1=SAT1,
            TPEH=TPEH,
            MVPA2=MVPA2,
            TP=TP,
            DGSI1=DGSI1,
            SAT2=SAT2,
            COR=COR,
            DGSI2=DGSI2,
            TS=TS,
            SG=SG,
        )
        status = analisar_risco(data)
        return status
    except Exception as e:
        return str(e)

@app.put("/pre_classificacao/update")
def put_pre_classificacao():
    gerar_arvore()
    return 1

@app.put("/pre_classificacao/gerar_fig")
def put_pre_classificacao_fig():
    status = gerar_img()
    return status