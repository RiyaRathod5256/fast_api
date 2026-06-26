# from fastapi import FastAPI,Query
# from pydantic import BaseModel
# from typing import Annotated

# app=FastAPI()



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



# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# app = FastAPI()


# @app.get("/items/")
# async def read_items(q: Annotated[str|None,Query()]= None):
#     results = {"items":[{"item_id":"Foo"},{"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
    
#     return results

# import random
# from typing import Annotated

# from fastapi import FastAPI
# from pydantic import AfterValidator

# app= FastAPI()

# data = {
#     "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
#     "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
#     "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
# }
# def check_valid_id(id: str):
#     if not id.startswith(("isbn-", "imdb-")):
#         raise ValueError(
#     'Invalid ID format, it must start with "isbn-" or "imdb-"'
# )
#     return id

# @app.get("/items/")
# async def read_items(id: Annotated[str|None,AfterValidator(check_valid_id)]=None):
#     if id:
#         item=data.get(id)
#     else:
#         id, item = random.choice(list(data.items()))
#     return {"id": id, "name": item}
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query