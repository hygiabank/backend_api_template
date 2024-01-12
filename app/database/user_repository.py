from functools import lru_cache

from app.utils.base_repo import BaseRepository

from .models import User


class UserRepository(BaseRepository):
    model = User
    related_models = []

@lru_cache
def get_user_repository() -> UserRepository:
    return UserRepository()
