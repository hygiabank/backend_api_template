from fastapi import FastAPI, APIRouter, Depends, Response, status
from fastapi import HTTPException

from app.controllers import read_users, read_user, create_user, update_user, delete_user, authenticate
from app.database.models import Plano, User
from app.schemas import CreateUserInput, CreateUserOutput
from app.security import set_token_cookie, revoke_token_cookie, get_current_user, hash_password, TokenData
from app.utils.validacao import is_valid_password


def create_login_router() -> APIRouter:
    router = APIRouter()

    @router.post("/login", status_code=status.HTTP_200_OK)
    async def login(username: str, password: str, response: Response) -> dict:
        user = await authenticate(username, password)
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
    async def create(input: CreateUserInput) -> dict:
        # Validação de senha
        if not is_valid_password(input.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Para sua segurança, crie uma senha com uma mistura de letras maiúsculas"
                                       " e minúsculas, números e símbolos especiais.")

        hashed_password = hash_password(input.password)
        new_user = await create_user(name=input.name, age=input.age, username=input.username, password=hashed_password, cpf=input.cpf)

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
        updated_user = await update_user(id=user_id, name=input.name, age=input.age, username=input.username,
                                         password=input.password)
        return updated_user

    @router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(user_id: str = Depends(get_current_user)) -> None:
        await delete_user(id=user_id)

    @router.post('/escolher-plano/{username}')
    async def escolher_plano(username: str, nome_plano: str):
        usuario = await User.get_or_none(username=username)
        plano = await Plano.get_or_none(nome=nome_plano)

        if not usuario or not plano:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário ou Plano não encontrado")

        usuario.plano = plano
        await usuario.save()
        return {"mensagem": "Plano escolhido com sucesso"}

    return router

    @router.get("/health-check", status_code=status.HTTP_200_OK)
    async def health_check() -> dict:
        return {"status": "API operacional"}

    return router


def init_routes(app: FastAPI):
    user_crud_router = create_rest_router()
    login_router = create_login_router()

    app.include_router(user_crud_router, prefix="/api", tags=["user"])
    app.include_router(login_router, prefix="/auth", tags=["authentication"])


app = FastAPI()
init_routes(app)
