from fastapi import FastAPI
from api.routers import users
from routers import products, users, users_db

app = FastAPI()  #Crea objeto de clase FastAPI, crea contexto de servidor

#Routers

app.include_router(products.router)
app.include_router(users.router)
app.include_router(users_db.router)

@app.get("/")   #hace una operacion get a una barra o en su momento a un url. La barra es la raiz del local host, solo puede haber una llamada a raiz
async def root():  #la función asincrona permite que esta instrucción se acomplete en segundo plano, deja que se ejecuten otras acciones
    return "Hola Dany, acabo de levantar mi propio servidor web"

#levanta servidor con uvicorn.. usa  uvicorn main:app --reload.
#uvicorn se instala con fastapi.. main es el nombre de fichero a arrancar y app es nuestro context
# el argumento --reload es par que si nosotros cambiamos algo en el fichero este se actualice sin tener que bajar el servidor y volverlo a arrancar
# despliega el servidor en un local host https://127.0.0.1:8000

@app.get("/url")
async def url():
    return { "url_curso": "https://cursohector.com/python"}
