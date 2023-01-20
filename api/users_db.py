from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.staticfiles import StaticFiles
from db.models.user import Users
from db.client import db_client
from db.schemas import user


router = APIRouter(prefix="/userdb", tags=["userdb"])

# router.mount("/static", StaticFiles(directory="static"), name="static") Nonta la imagen del archivo static/images

users_fake_db = []

@router.get("/")   
async def users():
    return users_fake_db

#PATH
@router.get("/{id}") #parametro de path, cuando el parámetro va en la url
async def user(id:int):
    return search_user(id)

#POST, para crear usuario
@router.post("/", status_code=201) #status code 201 status creado
async def user(user: Users):

    user_dict = dict(user)

    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id":id}))
    # if type(search_user(user.id)) == Users:
    #     raise HTTPException(status_code=204, detail="El usuario ya existe")
    #     #return {"error":"El usuario ya existe"}
    # else:
    #     users_fake_db.append(user)
    #     return {"status":"succeeded", "message":"El usuario se ha agregado con exito"}

    return Users(**new_user)

#PUT, actualizar o modificar usuario
@router.put("/")
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
@router.delete("/{id}")
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