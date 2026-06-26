from fastapi import FastAPI
from pydantic import BaseModel,Field,EmailStr,field_validator,model_validator

app=FastAPI()

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
        

user_list=list()
@app.post("/user/")
async def create_user(user: User):
    user_list.append(user.model_dump())
    return {
          "message":"User registered successfully",
          "user":{
                "username":user.username,
                "email":user.email
          }
    }
