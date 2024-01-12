from typing import Optional

from app.database.user_repository import UserRepository
from app.exceptions import Unauthorized
from app.security import authenticate_user


async def create_user(user_repository: UserRepository, **kwargs) -> dict:
    new_user = await user_repository.create(**kwargs)
    return {
        "id": new_user.id,
        "name": new_user.name,
        "age": new_user.age,
        "username": new_user.username,
    }


async def read_user(id: int, user_repository: UserRepository) -> dict:
    user = await user_repository.get(id=id)
    return {
        "id": user.id,
        "name": user.name,
        "age": user.age,
        "username": user.username,
    }


async def update_user(id: str, user_repository: UserRepository, **kwargs) -> dict:
    updated_user = await user_repository.update(id=id, **kwargs)
    return {
        "id": updated_user.id,
        "name": updated_user.name,
        "age": updated_user.age,
        "username": updated_user.username,
    }


async def delete_user(
    id: str,
    user_repository: UserRepository,
) -> None:
    return await user_repository.delete(id=id)


async def read_users(
    user_repository: UserRepository, skip: int = 0, limit: int = 100, filter_dict: Optional[dict] = None
) -> list[dict]:
    users = await user_repository.get_all(skip=skip, limit=limit, filter=filter_dict)
    return [
        {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "username": user.username,
        }
        for user in users
    ]


async def authenticate(username: str, password: str, user_repository: UserRepository) -> dict:
    user = await user_repository.get_by_username(username=username)
    if not user:
        raise Unauthorized("Invalid username")
    print(password)
    authenticate_user(password, user.password)
    return {
        "id": str(user.id),
        "name": user.name,
        "age": user.age,
        "username": user.username,
    }
