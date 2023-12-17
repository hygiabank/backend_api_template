from tortoise.models import Model
from tortoise import fields


class User(Model):
    class Meta:
        table = 'user'

    name = fields.TextField()
    birthdate = fields.DateField(null=True)
    age = fields.IntField(null=True)
    username = fields.CharField(unique=True, max_length=20)
    password = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    plano = fields.ForeignKeyField('models.Plano', related_name='usuarios', null=True)
    cpf = fields.CharField(max_length=11, unique=True, null=False)


class Plano(Model):
    id = fields.IntField(pk=True)
    nome = fields.CharField(max_length=50, unique=True)
    descricao = fields.TextField()

    class Meta:
        table = 'plano'
