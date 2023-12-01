from app.utils.base_repo import BaseRepository
from .models import User

class UserRepository(BaseRepository):
    model = User
    related_models = []


user_repository = UserRepository()