from pydantic import BaseModel, Field, EmailStr

class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    faculty: str = Field(min_length=2, max_length=100)
    semester: int = Field(ge =1, le =8)
    email: EmailStr 
    

class StudentResponse(BaseModel):
    id: int
    name: str
    faculty: str
    semester: int
    email: str

    model_config = {
        "from_attributes": True
    }
    
class StudentUpdate(BaseModel):
    name: str
    faculty: str
    semester: int
    email: EmailStr
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True
    }