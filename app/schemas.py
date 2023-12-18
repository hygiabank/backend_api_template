from pydantic import BaseModel


class CreateUserInput(BaseModel):
    name: str
    age: int
    username: str
    password: str
    cpf: str


class CreateUserOutput(BaseModel):
    id: int
    name: str
    age: int
    username: str
    cpf: str
