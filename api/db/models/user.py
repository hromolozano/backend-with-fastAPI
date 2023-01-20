from pydantic import BaseModel

class Users(BaseModel):  #Crea clase con BaseModel para poder decirle que argumentos debe llevar al inicar el objeto Users
    name:str
    surname:str
    id:int | None