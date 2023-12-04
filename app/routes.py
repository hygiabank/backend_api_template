from fastapi import FastAPI, APIRouter, Depends, Response, status
from app.security import set_token_cookie, revoke_token_cookie, get_current_user, hash_password, TokenData
from app.controllers import read_users, read_user, create_user, update_user, delete_user, return_user_statistics, authenticate
from app.schemas import CreateUserInput, CreateUserOutput, StatisticsOuput

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

    @router.get("/users-statistics", response_model=StatisticsOuput, status_code=status.HTTP_200_OK)
    async def get_user_stats(resample_time: int) -> dict:
        
        """
        Get User Statistics

        Param:
            resample_time (int): resample time to accumulate and show new users, in ms
        Output:
            dict: dict contaning StatisticsOuput: new_users_per_time, user_per_time_acc, average_user_age
        """

        return await return_user_statistics(resample_time=resample_time)

    return router

def init_routes(app: FastAPI):
    user_crud_router = create_rest_router()
    login_router = create_login_router()
    app.include_router(login_router, prefix="/api", tags=["login"])
    app.include_router(user_crud_router, prefix="/api", tags=["user"])