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
from sklearn.metrics import recall_score, precision_score, accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.svm import SVC

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
dn = pd.read_csv('./tables/NOME_DOENCAS.csv')
rf = None
y_test = None
x_test = None
x_train = None
y_train = None
previsoes = None

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

def adicionar_descricao(sintoma, nomecompleto, description):
    dn.insert(0, sintoma.upper(), None)
    dn[sintoma.upper()] = [nomecompleto, description]
    dn.to_csv('./tables/NOME_DOENCAS.csv', index=False)
    return 1

def gerar_arvore():
    X = df.drop('RISCO',axis=1)
    y = df['RISCO']
    global rf
    global y_test
    global x_test
    global x_train
    global y_train
    global previsoes

    X_tr, X_ts, y_tr, y_ts = train_test_split(X,y, test_size=0.30, random_state=61658)

    x_train = X_tr
    y_train = y_tr
    x_test = X_ts
    y_test = y_ts
    rf = RandomForestClassifier(max_depth=30, random_state=61658, n_estimators=10)
    rf.fit(X_tr, y_tr)
    previsoes = rf.predict(x_test)

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

def get_precisao():
    data = rf.predict(x_test)
    prec = {
        'accuracy_score': accuracy_score(y_test, data),
        'f1_score': f1_score(y_test, data, average='macro'),
        'precision_score': precision_score(y_test, data, average='macro'),
        'recall_score': recall_score(y_test, data, average='macro')
    }
    return prec

def get_matrix():
    cm = confusion_matrix(y_test, previsoes)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.show()

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
    global df
    df = pd.read_csv('./tables/TABELA_TCC.csv')
    lista_sintomas = list(df.columns)
    default = list(df.loc[0])
    paciente = {}
    for i in range(len(lista_sintomas)):
        paciente[lista_sintomas[i]] = default[i]
    return paciente

@app.get("/pre_classificacao/precisao")
def fornecer_precisao():
    try:
        global rf
        if rf is None:
            gerar_arvore()
        precisao = get_precisao()
        return precisao
    except Exception as e:
        return str(e)
    
@app.get("/pre_classificacao/gerar_matrix")
def gerar_matrix():
    try:
        global rf
        if rf is None:
            gerar_arvore()
        precisao = get_matrix()
        return precisao
    except Exception as e:
        return str(e)

@app.get("/pre_classificacao/nome_descricao_sintoma")
def get_name_description():
    global dn
    dn = pd.read_csv('./tables/NOME_DOENCAS.csv')
    lista_de_doencas = list(dn.columns)
    lista_de_colunas = [dn[col].tolist() for col in dn.columns]
    colunas = dn.columns.tolist()
    data = {}
    for i in range(len(lista_de_colunas)):
        data [colunas[i]] = lista_de_colunas[i]
    return data

@app.post("/pre_classificacao/post_csv_transposto")
def post_csv_transposto():
    # Carregue o arquivo CSV original
    df = pd.read_csv('./tables/NOME_DOENCAS.csv')
    # Transponha o DataFrame (linhas se tornam colunas e colunas se tornam linhas)
    df_transposto = df.transpose()
    # Salve o DataFrame transposto em um novo arquivo CSV
    df_transposto.to_csv('./tables/NOME_DOENCAS2.csv', index=False)

@app.post("/pre_classificacao/descricao")
def get_pre_classificacao(
    sintoma: str, nomecompleto: str, description: str, default: Union[int, bool]
):
    try:
        global rf
        if rf is None:
            gerar_arvore()
        status = adicionar_sintoma(sintoma, default)
        status = adicionar_descricao(sintoma, nomecompleto, description)
        return status
    except Exception as e:
        return str(e)
