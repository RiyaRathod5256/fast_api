from fastapi import FastAPI,HTTPException,Query,Path
from pydantic import BaseModel,Field,EmailStr,field_validator,model_validator
from pwdlib import PasswordHash
from typing import Annotated

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
        

user_list=[]
@app.post("/user/")
async def create_user(user: User):
    password_hash.hash(user.password)
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
        
                          
                     

@app.post("/login/")
async def login_user(user_cred:Userlogin):
             for i in user_list:
                if i["username"]==user_cred.username:
                          if password_hash.verify(user_cred.password,i["password"]):
                                 return {"msg":"login successfully"}
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