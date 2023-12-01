from dataclasses import dataclass
from pydantic import BaseModel
from typing import Type, TypeVar, Optional
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields import (
    BackwardFKRelation,
    BackwardOneToOneRelation,
    ManyToManyRelation,
    ReverseRelation,    
)

CreateModel = TypeVar("CreateModel", bound=BaseModel)
UpdateModel = TypeVar("UpdateModel", bound=BaseModel)
InDatabaseModel = TypeVar("InDatabaseModel", bound=BaseModel)

class CreateManyModel(BaseModel):
    items: list[CreateModel]

class UpdateManyModel(BaseModel):
    items: list[UpdateModel]

@dataclass(frozen=True, slots=True)
class PydanticModels:
    create: Type[CreateModel]
    update: Type[UpdateModel]
    read: Type[InDatabaseModel]
    create_many: Optional[Type[CreateManyModel]] = None
    update_many: Optional[Type[UpdateManyModel]] = None

class SchemaFactory():
    Config = dict(extra = 'ignore', from_attributes = True)

    @staticmethod
    def __get_relational_fields(model: Model):
        relational_fields = (
            BackwardFKRelation,
            BackwardOneToOneRelation,
            ManyToManyRelation,
            ReverseRelation,    
        )
        return [field_name for field_name, field_object in model._meta.fields_map.items()
                if isinstance(field_object, relational_fields)]

    @staticmethod
    def __get_foreign_key_fields(model: Model):
        return model._meta.fk_fields

    def create_create_schema(self, model: Type[Model], exclude_fields: tuple[str] = ()) -> CreateModel:
         return pydantic_model_creator(model, name=f"{model.__name__}Create", exclude_readonly=True, exclude=exclude_fields, model_config=self.Config)

    def create_update_schema(self, model: Type[Model], exclude_fields: tuple[str] = ()) -> UpdateModel:
        return pydantic_model_creator(model, name=f"{model.__name__}Update", exclude_readonly=True, exclude=exclude_fields, model_config=self.Config)

    def create_in_db_schema(self, model: Type[Model], exclude_fields: tuple[str] = ()) -> InDatabaseModel:
        exclude_fields_set = set(exclude_fields)
        relational_fields_set = set(self.__get_relational_fields(model))
        fk_fields_set = set(self.__get_foreign_key_fields(model))
        final_fields_set = exclude_fields_set.union(relational_fields_set).union(fk_fields_set)

        return pydantic_model_creator(model, name=f"{model.__name__}InDB", exclude=final_fields_set, model_config=self.Config)

    def create_create_many_schema(self, model: Type[Model], exclude_fields: tuple[str] = ()) -> CreateManyModel:
        CreateSchema = self.create_create_schema(model, exclude_fields)
        return CreateManyModel[CreateSchema]

    def create_update_many_schema(self, model: Type[Model], exclude_fields: tuple[str] = ()) -> UpdateManyModel:
        UpdateSchema = self.create_update_schema(model, exclude_fields)
        return UpdateManyModel[UpdateSchema]


schema_factory = SchemaFactory()

def create_schemas(model, schemas: PydanticModels = None, extended = False):
    CreateSchema = schema_factory.create_create_schema(model) if not schemas else schemas.create
    UpdateSchema = schema_factory.create_update_schema(model) if not schemas else schemas.update
    InDBSchema = schema_factory.create_in_db_schema(model) if not schemas else schemas.read
    
    if extended:
        CreateManySchema = schema_factory.create_create_many_schema(model) if not schemas else schemas. create_many
        UpdateManySchema = schema_factory.create_update_many_schema(model) if not schemas else schemas.update_many
    else:
        CreateManySchema = None
        UpdateManySchema = None

    return PydanticModels(CreateSchema, UpdateSchema, InDBSchema, CreateManySchema, UpdateManySchema)