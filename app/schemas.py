from pydantic import BaseModel 

class StudentCreate(BaseModel):
    name: str
    faculty: str
    semester: int
    email: str
    

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
    email: str