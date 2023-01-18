from fastapi import FastAPI, APIRouter

router = APIRouter(prefix="/products", tags=["products"]) #APIRouter, para enrutar esta api products y poderla trabajar desde la api de main. Si se indica el prefix ya no se debe indicar este en las siguientes dos urls de las operaciones

products_list = ["Producto1","Producto2"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id:int):
    return products_list[id]