from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,EmailStr,field_validator,model_validator
from pwdlib import PasswordHash

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
                       