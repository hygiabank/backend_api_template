from dataclasses import dataclass
from typing import Type, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from .base_repo import BaseRepository
from .schema_factory import PydanticModels, create_schemas

class DefaultCRUDParameters:
    @staticmethod
    async def get_all(skip: int = 0, limit: int = 100, filter_dict: Optional[dict] = None):
        return {"skip": skip, "limit": limit, "filter": filter_dict}

    @staticmethod
    async def get(id: int):
        return {"id": id}

    @staticmethod
    async def post(input: Type[BaseModel]):
        return input.model_dump()

    @staticmethod
    async def put(id: int, input: Type[BaseModel]):
        return {"id": id, **input.model_dump()}

    @staticmethod
    async def delete(id: int):
        return {"id": id}


@dataclass(frozen=True)
class CRUDParameters:
    GET_ALL: Optional[callable] = staticmethod(DefaultCRUDParameters.get_all)
    GET: Optional[callable] = staticmethod(DefaultCRUDParameters.get)
    POST: Optional[callable] = staticmethod(DefaultCRUDParameters.post)
    PUT: Optional[callable] = staticmethod(DefaultCRUDParameters.put)
    DELETE: Optional[callable] = staticmethod(DefaultCRUDParameters.delete)


def create_rest_router(
        repo: Type[BaseRepository],
        schemas: PydanticModels = None,
        params_parser: CRUDParameters = CRUDParameters
        ) -> APIRouter:
    
    router = APIRouter()

    model = repo.model
    model_name = model.__name__.lower()

    if not schemas:
        schemas = create_schemas(model, schemas)

    @router.get("/")
    async def read_all(repo_instance: BaseRepository = Depends(repo), params = Depends(params_parser.GET_ALL)) -> list[schemas.read]:
        return await repo_instance.get_all(**params)
        
    @router.get("/{%s_id}" % model_name)
    async def read(repo_instance: BaseRepository = Depends(repo), params = Depends(params_parser.GET)) -> schemas.read:
        return await repo_instance.get(**params)

    @router.post("/")
    async def create(input: schemas.create, repo_instance: BaseRepository = Depends(repo), params = Depends(params_parser.POST)) -> schemas.read:
        new_item = await repo_instance.create(**params)
        return schemas.read.model_validate(new_item)

    @router.put("/{%s_id}" % model_name)
    async def update(input: schemas.update, repo_instance: BaseRepository = Depends(repo), params = Depends(params_parser.PUT)) -> schemas.read:
        updated_item = await repo_instance.update(**params)
        return schemas.read.model_validate(updated_item)

    @router.delete("/{%s_id}" % model_name)
    async def delete(repo_instance: BaseRepository = Depends(repo), params = Depends(params_parser.DELETE)) -> None:
        await repo_instance.delete(**params)

    return router