from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

# body example
# {
#   "name":"Hector",
#   "surname":"Lozano",
#   "id":2
# }

router = APIRouter(prefix="/users", tags=["users"])

router.mount("/static", StaticFiles(directory="static"), name="static") #Nonta la imagen del archivo static/images

class Users(BaseModel):  #Crea clase con BaseModel para poder decirle que argumentos debe llevar al inicar el objeto Users
    name:str
    surname:str
    id:int

users_fake_db = [Users(name="Héctor",surname="Romo", id =1)] #esto podría representar la base de datos

@router.get("/")   
async def users():
    return users_fake_db

#QUERY
@router.get("/user/") #  cuando hay parametros que no van en esta url se les llama parámetro de query con /?{parameter}=
async def user(id:int):  # se pueden hacer 2 funcines una para que acepte el parametro id por path y otra para que tmb lo haga por query
    return search_user(id)

#PATH
@router.get("/user/{id}") #parametro de path, cuando el parámetro va en la url
async def user(id:int):
    return search_user(id)

#POST, para crear usuario
@router.post("/user/", status_code=201) #status code 201 status creado
async def user(user: Users):
    if type(search_user(user.id)) == Users:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
        #return {"error":"El usuario ya existe"}
    else:
        users_fake_db.append(user)
        return {"status":"succeeded", "message":"El usuario se ha agregado con exito"}

#PUT, actualizar o modificar usuario
@router.put("/user/")
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
@router.delete("/user/{id}")
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