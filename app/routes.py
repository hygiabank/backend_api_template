from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Response, status

from app.controllers import authenticate, create_user, delete_user, read_user, read_users, update_user
from app.database.user_repository import UserRepository, get_user_repository
from app.schemas import CreateUserInput, CreateUserOutput
from app.security import TokenData, get_current_user, hash_password, revoke_token_cookie, set_token_cookie


def create_login_router() -> APIRouter:
    router = APIRouter()

    @router.post("/login", status_code=status.HTTP_200_OK)
    async def login(
        username: str,
        password: str,
        response: Response,
        user_repository: Annotated[UserRepository, Depends(get_user_repository)]
    ) -> dict:
        user = await authenticate(username, password, user_repository)
        token_data = TokenData(sub=user['id'])
        token = set_token_cookie(token_data, response)

        return {"token": token, "token_type": "http-only cookie"}

    @router.post("/logout", status_code=status.HTTP_200_OK)
    async def logout(response: Response) -> dict:
        revoke_token_cookie(response)
        return {"message": "Logout successful"}

    return router


def create_rest_router() -> APIRouter:
    router = APIRouter()

    @router.post("/user", response_model=CreateUserOutput, status_code=status.HTTP_201_CREATED)
    async def create(
        input: CreateUserInput, user_repository: Annotated[UserRepository, Depends(get_user_repository)]
    ) -> dict:
        new_user = await create_user(
            name=input.name,
            age=input.age,
            username=input.username,
            password=hash_password(input.password),
            user_repository=user_repository,
        )
        return new_user

    @router.get("/users", response_model=list[CreateUserOutput], status_code=status.HTTP_200_OK)
    async def read_all(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
        skip: int = 0,
        limit: int = 100,
        filter: str = None,
        filter_value: str = None,
    ) -> list[dict]:
        filter_dict = {filter: filter_value} if filter else None
        return await read_users(skip=skip, limit=limit, filter_dict=filter_dict, user_repository=user_repository)

    @router.get("/user", response_model=CreateUserOutput, status_code=status.HTTP_200_OK)
    async def read(
        user_id: Annotated[str, Depends(get_current_user)],
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    ) -> dict:
        return await read_user(id=user_id, user_repository=user_repository)

    @router.put("/user", response_model=CreateUserOutput, status_code=status.HTTP_200_OK)
    async def update(
        input: CreateUserInput,
        user_id: Annotated[str, Depends(get_current_user)],
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    ) -> dict:
        updated_user = await update_user(
            id=user_id,
            name=input.name,
            age=input.age,
            username=input.username,
            password=input.password,
            user_repository=user_repository,
        )
        return updated_user

    @router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(
        user_id: Annotated[str, Depends(get_current_user)],
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    ) -> None:
        await delete_user(id=user_id, user_repository=user_repository)

    return router


def init_routes(app: FastAPI):
    user_crud_router = create_rest_router()
    login_router = create_login_router()
    app.include_router(login_router, prefix="/v1", tags=["login"])
    app.include_router(user_crud_router, prefix="/v1", tags=["user"])
