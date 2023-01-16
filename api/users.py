from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Users(BaseModel):  #Crea clase con BaseModel para poder decirle que argumentos debe llevar al inicar el objeto Users
    name:str
    surname:str
    id:int

users_fake_db = [Users(name="Héctor",surname="Romo", id =1)] #esto podría representar la base de datos


@app.get("/users")   
async def users():
    return users_fake_db

#QUERY
@app.get("/user/") # parametro de path, cuando hay parametros que no van en esta url se les llama parámetro de query con /?{parameter}=
async def user(id:int):  # se pueden hacer 2 funcines una para que acepte el parametro id por path y otra para que tmb lo haga por query
    return search_user(id)

#PATH
@app.get("/user/{id}")
async def user(id:int):
    return search_user(id)

#POST
@app.post("/user/")
async def user(user: Users):
    if type(search_user(user.id)) == Users:
        return {"error":"El usuario ya existe"}
    else:
        users_fake_db.append(user)
        return {"status":"succeeded", "message":"El usuario se ha agregado con exito"}

#PUT
@app.put("/user/")
async def user(user: Users):
    found = False
    for index, saved_user in enumerate(users_fake_db):
        if saved_user.id == user.id:
            users_fake_db[index] = user
            found = True
    if not found:
        return {"error":"El usuario no se ha actualizado"}
    else:
        return user

#DELETE
@app.delete("/user/{id}")
async def user(id:int):
    found = False
    for index, saved_user in enumerate(users_fake_db):
        if saved_user.id == id:
            del users_fake_db[index]
            found = True
    if found:
        return {"message":"Se ha eliminado el usuario correctamente"}
    else:
        return {"message":"El usuario no se ha eliminado porque no existe"}


def search_user(id:int):
    users = filter(lambda user: user.id == id, users_fake_db)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}