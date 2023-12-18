from fastapi import FastAPI, APIRouter, Depends, Response, status
from app.security import set_token_cookie, revoke_token_cookie, get_current_user, hash_password, TokenData
from app.controllers import (
    read_users, read_user, 
    create_user, update_user, 
    delete_user, authenticate, 
    read_tasks, create_task, 
    read_task, update_task,
    delete_task
)
from app.schemas import CreateUserInput, CreateUserOutput, TaskOutput, TaskInput

def create_login_router() -> APIRouter:
    router = APIRouter()

    @router.post("/login", status_code=status.HTTP_200_OK)
    async def login(username: str, password: str, response: Response) -> dict:
        user = await authenticate(username, password)
        token_data = TokenData(sub=user['id'])
        token = set_token_cookie(token_data, response)

        return { "token": token, "token_type": "http-only cookie" }

    @router.post("/logout", status_code=status.HTTP_200_OK)
    async def logout(response: Response) -> dict:
        revoke_token_cookie(response)
        return { "message": "Logout successful" }

    return router

def create_rest_router() -> APIRouter:
    router = APIRouter()

    @router.post("/user", response_model=CreateUserOutput, status_code=status.HTTP_201_CREATED)
    async def create(input: CreateUserInput) -> dict:
        new_user = await create_user(name=input.name, age=input.age, username=input.username, password=hash_password(input.password))
        return new_user

    @router.get("/users", response_model=list[CreateUserOutput], status_code=status.HTTP_200_OK)
    async def read_all(skip: int = 0, limit: int = 100, filter: str = None, filter_value: str = None) -> list[dict]:
        filter_dict = {filter: filter_value} if filter else None
        return await read_users(skip=skip, limit=limit, filter_dict=filter_dict)

    @router.get("/user", response_model=CreateUserOutput, status_code=status.HTTP_200_OK)
    async def read(user_id: str = Depends(get_current_user)) -> dict:
        return await read_user(id=user_id)

    @router.put("/user", response_model=CreateUserOutput, status_code=status.HTTP_200_OK)
    async def update(input: CreateUserInput, user_id: str = Depends(get_current_user)) -> dict:
        updated_user = await update_user(id=user_id, name=input.name, age=input.age, username=input.username, password=input.password)
        return updated_user

    @router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(user_id: str = Depends(get_current_user)) -> None:
        await delete_user(id=user_id)

    return router

def create_rest_router_tasks() -> APIRouter:
    router = APIRouter()

    @router.post("/task", response_model=TaskOutput, status_code=status.HTTP_201_CREATED)
    async def create(input: TaskInput, user_id: int = Depends(get_current_user)) -> dict:
        task = await create_task(name=input.name, description=input.description, user_id=user_id)
        return task
    
    @router.get("/task", response_model=TaskOutput, status_code=status.HTTP_200_OK)
    async def read(id: int, user_id: int = Depends(get_current_user)) -> dict:
        return await read_task(id=id, user_id=user_id)
    
    @router.put("/task", response_model=TaskOutput, status_code=status.HTTP_200_OK)
    async def update(input: TaskInput, id: int, user_id: int = Depends(get_current_user)) -> dict:
        task = await update_task(id=id, name=input.name, description=input.description, user_id=user_id)
        return task
    
    @router.delete("/task", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(id: int, user_id: int = Depends(get_current_user)) -> None:
        await delete_task(id=id, user_id=user_id)
    
    @router.get("/tasks", response_model=list[TaskOutput], status_code=status.HTTP_200_OK)
    async def read_all(skip: int = 0, limit: int = 100, user_id: int = Depends(get_current_user)) -> list[dict]:
        return await read_tasks(skip=skip, limit=limit, user_id=user_id)
    
    return router



def init_routes(app: FastAPI):
    user_crud_router = create_rest_router()
    login_router = create_login_router()
    task_router = create_rest_router_tasks()
    
    app.include_router(login_router, prefix="/api", tags=["login"])
    app.include_router(user_crud_router, prefix="/api", tags=["user"])
    app.include_router(task_router, prefix="/api", tags=["task"])