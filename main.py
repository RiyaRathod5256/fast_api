from fastapi import FastAPI,HTTPException,Query,Path,Body,Response,Cookie,Depends
from pydantic import BaseModel,Field,EmailStr,field_validator,model_validator,fields,HttpUrl
from pwdlib import PasswordHash
from typing import Annotated
from datetime import datetime,time,timedelta
from uuid import UUID
import uuid

app=FastAPI()
password_hash = PasswordHash.recommended()

class User(BaseModel):
    
    username:str=Field(pattern=r"^[a-zA-Z0-9_]{3,20}$")
    email:EmailStr
    password:str=Field(min_length=8,max_length=8)
    confirm_password:str=Field(min_length=8,max_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls,value:str):
        if not any(c.isupper() for c in value):
                raise ValueError("Password must contain at least one uppercase letter")

        if not any(c.islower() for c in value):
                raise ValueError("Password must contain at least one lowercase letter")

        if not any(c.isdigit() for c in value):
                raise ValueError("Password must contain at least one digit")

        if not any(c in "@$!%*?&" for c in value):
                raise ValueError(
                    "Password must contain at least one special character (@$!%*?&)"
                )
        return value
        
    @model_validator(mode="after")
    def passwords_match(self):
           if self.password != self.confirm_password:
                    raise ValueError("Password do not match")
           return self
        

user_list=[{'user_id': 1, 'username': 'riya', 'email': 'riya@gmail.com', 'password': '$argon2id$v=19$m=65536,t=3,p=4$Vzz0EQE+TLnwif4skryK3w$7tOTBPzrkN4R4nAX9odNNQ8NTlVAGu4/+YME2JwpJRY'}]
@app.post("/user/")
async def create_user(user: User):
    
    data={
           "user_id":len(user_list)+1,
           "username":user.username,
           "email":user.email,
           "password":password_hash.hash(user.password)
    }
    user_list.append(data)
    print(user_list)

    return {
          "message":"User registered successfully",
          "user":{
                "username":user.username,
                "email":user.email
          }
    }
class Userlogin(BaseModel):
       username:str
       password:str
        
                          
                     
sessions={"865c46be-ed39-4b90-bfd7-f1026e46622c":"riya"}
@app.post("/login/")
async def login_user(user_cred:Userlogin,response:Response):
             for i in user_list:
                if i["username"]==user_cred.username:
                          if password_hash.verify(user_cred.password,i["password"]):
                                 session_id=str(uuid.uuid4())
                                 sessions[session_id] = i["username"]

                                 response.set_cookie(
                                        key="session_id",
                                        value=session_id,
                                        httponly=True,
                                        max_age=3600
                                        
                                 )
                                 
                                 return {"msg":"login successfully",
                                         "session_id":session_id}
                          else:
                                 raise HTTPException(status_code=404,detail="invalid user")
                                 
             else:
                    raise HTTPException(status_code=404,detail="User not found")
task=[{"task_id":1,"task_name":"updateapi","task_status":"completed"},{"task_id":2,"task_name":"github","task_status":"pending"}]
@app.get("/task/{task_id}")
async def task_read(task_id: Annotated[int,Path(gt=0,lt=20)]):
       for i in task:
              if i.get("task_id")==task_id:
                     return i
              else:
                     return {"msg":"task does not exist"}
class Taskupdate(BaseModel):
       task_name:str
       task_status:str

@app.put("/task_update/{task_id}")
async def task_update(task_id: int,task_update:Taskupdate):
       for i in task:
              if i.get("task_id")==task_id:
                     i["task_name"]=task_update.task_name
                     i["task_status"]=task_update.task_status
                     return("task updated successfully")
              else:
                     return("task does not exist")
class Taskfield(BaseModel):
       task_name:str|None=None
       task_status:str|None=None     
@app.patch("/task/{task_id}")
async def update_field(task_id:int,task_field:Taskfield):
       for i in task:
              if i.get("task_id") == task_id:
                     updated_fields=task_field.model_dump(exclude_unset=True)
                     for key,value in updated_fields.items():
                            i[key]=value
                     return {"key updated successfully"}    
       else:
              return{"task does not exist"}        
       
@app.delete("/delete/{task_id}")
async def delete_fields(task_id:int):
       for i in task:
              if i.get("task_id")==task_id:
                     task.remove(i)
                     return{"task deleted succesfully"}
       else:
              raise HTTPException(status_code=404,detail="task not found")

class Customer(BaseModel):
       Customer_name:str
       Customer_email:str



class Task_create(BaseModel):
       Task_title:str
       Task_status:str


@app.post("/Customer/")
async def Customer_register(customer:Customer=Body(),task:Task_create=Body()):
       return{
              "msg":"customer and task created"
       }

# class Item(BaseModel):
#     name: str
#     description: str | None = Field(
#         default=None, title="The description of the item", max_length=300
#     )
#     price: float = Field(gt=0, description="The price must be greater than zero")
#     tax: float | None = None


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
#     results = {"item_id": item_id, "item": item}
#     return results

# class Image(BaseModel):
#     url: HttpUrl
#     name: str


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()
#     image: Image | None = None


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results

# from fastapi import FastAPI
# from pydantic import BaseModel, HttpUrl

# app = FastAPI()


# class Image(BaseModel):
#     url: HttpUrl
#     name: str


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()
#     images: list[Image] | None = None


# class Offer(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     items: list[Item]


# @app.post("/offers/")
# async def create_offer(offer: Offer):
#     return offer

# 



# class Item(BaseModel):
#     name: str = Field(examples=["Foo"])
#     description: str | None = Field(default=None, examples=["A very nice Item"])
#     price: float = Field(examples=[35.4])
#     tax: float | None = Field(default=None, examples=[3.2])


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results




# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int,
#     item: Annotated[
#         Item,
#         Body(
#             examples=[
#                 {
#                     "name": "Foo",
#                     "description": "A very nice Item",
#                     "price": 35.4,
#                     "tax": 3.2,
#                 }
#             ],
#         ),
#     ],
# ):
#     results = {"item_id": item_id, "item": item}
#     return results

# @app.put("/items/{item_id}")
# async def read_items(
#     item_id: UUID,
#     start_datetime: Annotated[datetime, Body()],
#     end_datetime: Annotated[datetime, Body()],
#     process_after: Annotated[timedelta, Body()],
#     repeat_at: Annotated[time | None, Body()] = None,
# ):
#     start_process = start_datetime + process_after
#     duration = end_datetime - start_process
#     return {
#         "item_id": item_id,
#         "start_datetime": start_datetime,
#         "end_datetime": end_datetime,
#         "process_after": process_after,
#         "repeat_at": repeat_at,
#         "start_process": start_process,
#         "duration": duration,
#     }


def get_user(session_id:Annotated[str|None,Cookie()]=None):
       
       user=sessions.get(session_id)
       if not user:
              raise HTTPException(401)
       return user

@app.get("/profile")
async def profile(user=Depends(get_user)):
       return{
               "message": "Welcome",
        "user": user

       }