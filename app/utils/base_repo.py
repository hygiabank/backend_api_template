from typing import Any, Optional, Type, TypeVar

from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.models import Model

from ..exceptions import ResourceAlreadyExists, ResourceNotFound

M = TypeVar('M', bound=Model)

class BaseRepository:
    model: Type[Model]
    related_models: list[str] = []

    def __error_message(self) -> str:
        return f"{self.model.__name__}"

    async def get_all(
            self, 
            *,
            skip: int = 0, 
            limit: int = 100, 
            filter: Optional[dict[str, Any]] = None
        ) -> list[Model]:

        items = self.model.all().prefetch_related(*self.related_models)

        if skip:
            items = items.offset(skip)
        
        if limit:
            items  = items.limit(limit)

        if filter:
            items = items.filter(**filter)
                
        return await items

    async def filter(self, **filter: dict[str, Any]) -> Model:
        try:
            query = self.model.get(**filter)
            if self.related_models:
               query.prefetch_related(*self.related_models)
            item = await query

        except DoesNotExist:
            raise ResourceNotFound(self.__error_message())

        return item

    async def get(self, id: int) -> Model:
        try:
            query = self.model.get(id=id)
            
            if self.related_models:
                query.prefetch_related(*self.related_models)
            
            item = await query

        except DoesNotExist:
            raise ResourceNotFound(self.__error_message())

        return item
    
    async def get_by_username(self, username: str) -> Model | None:
        query = self.model.get(username=username)
        return await query


    async def create(self, **kwargs: dict[str, Any]) -> Model:
        try:
            new_item = await self.model.create(**kwargs)
        except DoesNotExist as e:
            print(f"DoesNotExist: {e}")
        except IntegrityError as e:
            raise ResourceAlreadyExists(self.__error_message())
        
        return new_item

    async def update(self, id: int, **kwargs: dict[str, Any]) -> None:
        try:
            await self.model.filter(id=id).update(**kwargs)
            updated_item = await self.model.get(id=id)
        except DoesNotExist:
            raise ResourceNotFound(self.__error_message())

        return updated_item
    
    async def delete(self, id: int) -> None:
        try:
            await self.model.filter(id=id).delete()
        except DoesNotExist:
            raise ResourceNotFound(self.__error_message())
