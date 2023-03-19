from logging import exception
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Optional

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import plot_tree

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

def adicionar_paciente(data: dict, risco = None):
    if risco is None:
        risco = analisar_risco(data)

    values = list(data.values())
    values.append(risco)
    df.loc[len(df)] = values
    df.to_csv('./tables/TABELA_TCC.csv', index=False)
    return 1

def adicionar_sintoma(sintoma:str, default):
    if default == True:
        default = 1
    if default == False:
        default = 0

    df.insert(0, sintoma.upper(), default)
    df.to_csv('./tables/TABELA_TCC.csv', index=False)
    return 1

def gerar_arvore():
    X = df.drop('RISCO',axis=1)
    y = df['RISCO']
    global rf

    X_tr, X_ts, y_tr, y_ts = train_test_split(X,y, test_size=0.30, random_state=61658)

    rf = RandomForestClassifier(max_depth=22, random_state=61658, n_estimators=10)
    rf.fit(X_tr, y_tr)

def gerar_img():
    for x in range(len(rf.estimators_)):
        plt.figure(figsize=(75,20))
        plot_tree(rf.estimators_[x],filled=True)
        plt.savefig(f"./../../Anexos/figura_{x + 1}.jpg")
    return 1

def analisar_risco(data: dict):
    if 'RISCO' in data:
        data.pop('RISCO')

    lista_sintomas = list(df.columns)
    lista_sintomas.pop(-1)
    keys = list(data.keys())
    if lista_sintomas != keys:
        raise Exception("lista de sintomas fornecida incorretamente")
    
    values = list(data.values())
    amostra = []
    amostra.append(values)
    data = rf.predict(amostra)
    return int(data[0])

@app.put("/pre_classificacao/read")
def get_pre_classificacao(data: dict):
    try:
        global rf
        if rf is None:
            gerar_arvore()
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

@app.post("/pre_classificacao/paciente")
def get_pre_classificacao(
    paciente: dict, risco: int = None
):
    try:
        global rf
        if rf is None:
            gerar_arvore()
        status = adicionar_paciente(paciente, risco)
        return status
    except Exception as e:
        return str(e)
    
@app.post("/pre_classificacao/sintoma")
def get_pre_classificacao(
    sintoma: str, default: Union[int, bool]
):
    try:
        global rf
        if rf is None:
            gerar_arvore()
        status = adicionar_sintoma(sintoma, default)
        return status
    except Exception as e:
        return str(e)
    
@app.get("/pre_classificacao/paciente_default")
def get_sintomas():
    lista_sintomas = list(df.columns)
    default = list(df.loc[0])
    paciente = {}
    for i in range(len(lista_sintomas)):
        paciente[lista_sintomas[i]] = default[i]
    return paciente