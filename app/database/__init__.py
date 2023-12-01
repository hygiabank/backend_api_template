from tortoise.contrib.fastapi import register_tortoise
from app.settings import settings

TORTOISE_ORM = {
        'connections': 
        {
            'default': 
            {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {
                    "host": settings.DB_HOST,
                    "port": settings.DB_PORT,
                    "user": settings.DB_USERNAME,
                    "database": settings.DB_DATABASE,
                    "password": settings.DB_PASSWORD
                }
            },
        },
        "apps": {
            "models": {
                "models": ['app.database.models', 'aerich.models'],
                "default_connection": "default",
            },
        },
    }

def init_db(app):
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=settings.DEBUG,
        add_exception_handlers=settings.DEBUG,
    )