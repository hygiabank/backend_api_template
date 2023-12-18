from pydantic import BaseModel

class CreateUserInput(BaseModel):
    name: str
    age: int
    username: str
    password: str

class CreateUserOutput(BaseModel):
    id: int
    name: str
    age: int
    username: str


class TaskOutput(BaseModel):
    id: int
    name: str
    description: str
    

class TaskInput(BaseModel):
    name: str
    description: str