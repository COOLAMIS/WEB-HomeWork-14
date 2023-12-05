from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserModel(BaseModel):
    firstname: str
    secondname: str
    email: EmailStr
    phonenumber: str
    birthday: str

class UserSignUpModel(BaseModel):
    username: str
    password: str
    
class UserResponce(BaseModel):
    id: int = 1
    firstname: str
    secondname: str
    email: EmailStr
    phonenumber: str
    birthday: datetime

    class Config:
        orm_mode = True

