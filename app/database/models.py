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
