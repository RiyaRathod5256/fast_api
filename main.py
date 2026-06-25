from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()



# from enum import Enum
     
# # @app.get("/items/{item_id}")
# # async def read_item(item_id:int):
# #     return {"item_id":item_id}

# class ModelName(str,Enum):
#     alexnet="alexnet"
#     resnet="resnet"
#     lenet="lenet"

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
#     if model_name.value == "lenet":
#         return {"model_name":model_name,"message":"LeCNN all the images"}
    
#     return {"model_name": model_name, "message": "Have some residuals"}


# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return {
#         "file_path": file_path
#     }

fake_items_db=[{"item_name":{"Tshirt":"XL"}},{"item_name":{"Kurti":"XL"}},{"item_name":{"Baz":"L"}}]

# @app.get("/items/{item_id}")
# async def read_item(item_id: str,q: str| None = None,short: bool=False):
#     item={"item_id": item_id}
#     if q:
#         item.update({"q":q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item



# @app.get("/items/{item_id}")
# async def read_user_item(
#     item_id: str, needy: str, skip: int , limit: int | None = None
# ):
#     item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
#     return item
# fake_items_db={1:{"Tshrt":{"XL"}},2:{"Kurti":{"XL"}},3:{"Baz":{"L"}}}

# @app.get("/items/{item_id}")
# async def read_item(
#     item_id:int,
#     needy:str,
#     skip: int,
#     limit: int
# ):
#     return fake_items_db[item_id]


from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict