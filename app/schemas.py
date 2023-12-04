from pydantic import BaseModel

class CreateUserInput(BaseModel):
    name: str
    age: int
    username: str
    password: str
    creation_timestamp: float

class CreateUserOutput(BaseModel):
    id: int
    name: str
    age: int
    username: str
    
class StatisticsOuput(BaseModel):
    new_user_per_time: list
    user_per_time_acc: list
    average_user_age: float