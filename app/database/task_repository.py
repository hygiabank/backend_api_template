from app.utils.base_repo import (
    BaseRepository,
    ResourceNotFound,
    DoesNotExist,
    Model,
    Any
)
from .models import Task, User 

class TaskRepository(BaseRepository):
    model = Task
    related_models = []
    
    def __error_message(self) -> str:
        return f"{self.model.__name__}"
    
    async def create(self, **kwargs: dict[str, Any]) -> Model:
        try:
            user: User = await User.get(id=kwargs.get('user_id'))
        except DoesNotExist as e:
            raise ResourceNotFound(self.__error_message())
            
        new_item = await self.model.create(user=user, **kwargs)
        
        return new_item
    
    async def get(self, id: int, user_id: int) -> Model:
        try:
            query = self.model.get(id=id, user__id=user_id)
                
            if self.related_models:
                query.prefetch_related(*self.related_models)
            
            item = await query
            
        except DoesNotExist:
            raise ResourceNotFound(self.__error_message())

        return item
    
    async def update(self, id: int, **kwargs: dict[str, Any]) -> None:
        try:
            user: User = await User.get(id=kwargs.get('user_id'))
        except DoesNotExist as e:
            raise ResourceNotFound(self.__error_message())
            
        try:
            await self.model.filter(id=id, user=user).update(**kwargs)
            updated_item = await self.model.get(id=id, user=user)
        except DoesNotExist:
            raise ResourceNotFound(self.__error_message())

        return updated_item
    
    async def delete(self, id: int, user_id: int) -> None:
        await self.model.filter(id=id, user=user_id).delete()

task_repository = TaskRepository()