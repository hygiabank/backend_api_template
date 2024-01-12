import pytest

from app.controllers import authenticate, create_user, delete_user, read_user, read_users, update_user
from app.exceptions import Unauthorized

from tests.conftest import UserModel


class TestCreateUser:
    async def test_create_user(self, mock_user_repository, input_user, user_model):
        mock_user_repository.create.return_value = user_model

        result = await create_user(**input_user, user_repository=mock_user_repository)

        assert result == {
            "id": "1",
            "name": "John",
            "age": 25,
            "username": "john_doe",
        }
        mock_user_repository.create.assert_called_once_with(**input_user)


class TestReadUser:
    async def test_read_user_successfully(self, mock_user_repository, user_model):
        mock_user_repository.get.return_value = user_model

        result = await read_user(id=1, user_repository=mock_user_repository)

        assert result == {
            "id": "1",
            "name": "John",
            "age": 25,
            "username": "john_doe",
        }
        mock_user_repository.get.assert_called_once_with(id=1)


class TestUpdateUser:
    async def test_update_user(self, mock_user_repository, input_user, user_model):
        mock_user_repository.update.return_value = user_model

        result = await update_user(id=1, user_repository=mock_user_repository, **input_user)

        assert result == {
            "id": "1",
            "name": "John",
            "age": 25,
            "username": "john_doe",
        }
        mock_user_repository.update.assert_called_once_with(id=1, **input_user)


class TestDeleteUser:
    async def test_delete_user(self, mock_user_repository):
        await delete_user(id=1, user_repository=mock_user_repository)
        mock_user_repository.delete.return_value = None

        mock_user_repository.delete.assert_called_once_with(id=1)


class TestReadUsers:
    async def test_read_users(self, mock_user_repository):
        user_data_list = [
            {"id": "1", "name": "John", "age": 25, "username": "john_doe"},
            {"id": "2", "name": "Alice", "age": 30, "username": "alice_smith"},
        ]
        mock_user_repository.get_all.return_value = [UserModel(**data) for data in user_data_list]

        result = await read_users(user_repository=mock_user_repository)

        assert result == user_data_list
        mock_user_repository.get_all.assert_called_once_with(skip=0, limit=100, filter=None)


class TestAuthenticate:
    async def test_authenticate(self, user_model, mock_user_repository, mock_authenticate_user):
        mock_user_repository.get_by_username.return_value = user_model
        mock_authenticate_user.return_value = None

        result = await authenticate("john_doe", "password", mock_user_repository)

        assert result == {
            "id": "1",
            "name": "John",
            "age": 25,
            "username": "john_doe",
        }
        mock_user_repository.get_by_username.assert_called_once_with(username="john_doe")
        mock_authenticate_user.assert_called_once_with("password", user_model.password)

    async def test_authenticate_invalid_username(self, mock_user_repository):
        mock_user_repository.get_by_username.return_value = None

        with pytest.raises(Unauthorized, match="Invalid username"):
            await authenticate("nonexistent_user", "password", user_repository=mock_user_repository)

    async def test_authenticate_invalid_password(self, user_model, mock_user_repository, mock_authenticate_user):
        mock_user_repository.get.return_value = user_model
        mock_authenticate_user.side_effect = Unauthorized("Invalid password")

        with pytest.raises(Unauthorized, match="Invalid password"):
            await authenticate("john_doe", "incorrect_password", user_repository=mock_user_repository)
