from fastapi import FastAPI
from pydantic import BaseModel

from requests.api import post

app = FastAPI()

model = {}

class PostModel(BaseModel):
    id: int
    Titulo: str
    Autor: str
    Conteudo: str

@app.get("/blog/read")
def get_posts():
    d = model.values()
    d = list(d)
    return d

@app.get("/blog/read/{post_id}")
def get_one_post(post_id: int):
    d = model.keys()
    d = list(d)
    if post_id in d:
        return model[post_id]
    return {"message": "Post não existente!"}

@app.post("/blog/add/")
def add_post(post: PostModel):
    post_id = post.id
    d = model.keys()
    d = list(d) 
    if post_id in d:
        return {"message": "Post já existente!"}
    model[post_id] = post
    return {"message": "Post foi adicionado com Sucesso!"}

@app.put("/blog/update/{post_id}")
def update_post(post_id: int, post: PostModel):
    d = model.keys()
    d = list(d) 
    if post_id in d:
        model[post_id] = post
        return {"message": "Post foi atualizado com sucesso!"}
    return {"message": "Post não existente!"}

@app.delete("/blog/del/{post_id}")
def delete_post(post_id: int):
    d = model.keys()
    d = list(d) 
    if post_id in d:
        del model[post_id]
        return {"message": "Post foi deletado com sucesso!"}
    return {"message": "Post não existente!"}
