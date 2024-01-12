from dataclasses import dataclass
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import Response


@dataclass()
class UserModel:
    id: str
    name: str
    age: int
    username: str
    password: str = "fake_password"


@pytest.fixture
def input_user():
    return {"name": "John", "age": 25, "username": "john_doe", "password": "secure_password"}


@pytest.fixture
def db_user(input_user):
    return {**input_user, "id": "1"}


@pytest.fixture
def user_model(db_user):
    return UserModel(**db_user)


@pytest.fixture
def mock_response():
    return Mock(spec=Response)


@pytest.fixture
def mock_user_repository():
    return AsyncMock()


@pytest.fixture
def mock_authenticate_user():
    with patch('app.controllers.authenticate_user') as mock_authenticate:
        yield mock_authenticate
