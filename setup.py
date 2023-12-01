from setuptools import setup, find_packages

setup(
    name="backend",
    version="0.1",
    packages=find_packages(),
    package_dir={'app': 'app'},
    install_requires=[
        'aerich',
        'fastapi',
        'uvicorn',
        'python-multipart',
        'pydantic',
        'pydantic-settings',
        'tortoise-orm[asyncpg]',
        'python-jose[cryptography]',
        'bcrypt==4.0.1',
        'passlib',
    ],
)
