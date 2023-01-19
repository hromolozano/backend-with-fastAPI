from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth = OAuth2PasswordBearer(tokenUrl="login")  #Operacion que gestionara la autenticacion

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "Hector": {
        "username":"hromo95",
        "full_name":"Hector Manuel Romo Lozano",
        "email": "elbicho@gmail.com",
        "disabled":False,
        "password":"123123"
    },
    "Hector2": {
        "username":"pegasus",
        "full_name":"Hector Manuel Romo Lozano",
        "email": "fulanito@gmail.com",
        "disabled":True,
        "password":"asdfasdf"
    }
}

def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
@app.post("/login") #Operación de la API que se encargará de la autenticación y generará token
async def login(form:OAuth2PasswordRequestForm = Depends()): #Argumento: será la "forma" de tipo OAuth que tendra el user y password
    user_db = users_db.get(form.username ) #Buscar el username que viene desde form en el objeto de users_db. Si está asigna ese dict a users_db
    if not user_db:
        raise HTTPException(status_code=400, detail= "El usuario no es correcto")

    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail= "La contraseña es incorrecta")

    return {"access_token":user.username, "token_type":"bearer"}

async def current_user(token: str = Depends(oauth)): #Se le manda un token de tipo bearer y buscar en la users_db este username
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=401, detail= "El usuario no es correcto")
    return user
    

@app.get("/users/me")
async def me(user:User= Depends(current_user)):  #el argumento user será igual a un User (de tipo class User) que devuelve la operacion current_user
    return user
