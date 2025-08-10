from pydantic import BaseModel

from typing import Optional


class SignUpschema(BaseModel):
    email: str
    password : str

    class Config:
            json_schema_extra = {
                "example":  
                    {
                        "email": "sample@gmail.com",
                        "password": "Sample@123",
                    }
                
            }



class Loginschema(BaseModel):
    email : str
    password: str

    class Config:
            json_schema_extra = {
                "example": 
                    {
                        "email": "sample@gamil.com",
                        "password": "Sample@123",
                    }
                
            }


class ToDoCreate(BaseModel):
    task: str
    completed: bool = False
    timestamp: Optional[str] = None

class ToDoUpdate(BaseModel):
    task: Optional[str] = None
    completed: Optional[bool] = None
    timestamp: Optional[str] = None
