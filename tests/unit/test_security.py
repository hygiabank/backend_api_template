from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from freezegun import freeze_time
from jose import JWTError

from app.exceptions import Unauthorized
from app.security import (
    TokenData,
    authenticate_user,
    create_token,
    decode_token,
    get_current_user,
    hash_password,
    revoke_token_cookie,
    set_token_cookie,
    verify_password,
)
from app.settings import settings

DATA = {"sub": "1"}


class TestCreateToken:
    def test_create_token(self):
        token = create_token(DATA)
        assert isinstance(token, str)

    @patch("app.security.jwt.encode")
    @freeze_time("2024-01-12T06:53:05.263965")
    def test_create_token_with_expiration(self, mock_jwt_encode):
        expires_delta = timedelta(minutes=30)
        expected_exp = datetime.utcnow() + expires_delta

        mock_jwt_encode.return_value = "dummy_token"

        result = create_token(DATA, expires_delta)

        mock_jwt_encode.assert_called_once_with(
            {**DATA, "exp": expected_exp}, settings.JWT_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        assert result == "dummy_token"

    @patch("app.security.jwt.encode")
    @freeze_time("2024-01-12T06:53:05.263965")
    def test_create_token_without_expiration(self, mock_jwt_encode):
        expected_exp = datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRES)
        mock_jwt_encode.return_value = "dummy_token"

        result = create_token(DATA)

        mock_jwt_encode.assert_called_once_with(
            {**DATA, "exp": expected_exp}, settings.JWT_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        assert result == "dummy_token"


class TestDecodeToken:
    data = {"sub": "1"}

    def test_decode_token(self):
        token = create_token(DATA)
        decoded_data = decode_token(token)
        assert decoded_data.sub == "1"

    @patch('app.security.jwt.decode')
    def test_decode_token_valid(self, mock_jwt_decode):
        mock_jwt_decode.return_value = DATA

        result = decode_token('mock_token')

        mock_jwt_decode.assert_called_once_with(
            'mock_token', settings.JWT_AUTH_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )

        assert isinstance(result, TokenData)
        assert result.sub == "1"

    @patch('app.security.jwt.decode', side_effect=JWTError('Invalid token'))
    def test_decode_token_invalid(self, mock_jwt_decode):
        with pytest.raises(Unauthorized, match='Could not validate credentials: Invalid token'):
            decode_token('invalid_token')

        mock_jwt_decode.assert_called_once_with(
            'invalid_token', settings.JWT_AUTH_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )


class TestSetTokenCookie:
    @patch('app.security.create_token', return_value="mock_token")
    def test_set_token_cookie(self, mock_create_token, mock_response):
        set_token_cookie(TokenData(**DATA), mock_response)
        mock_response.set_cookie.assert_called_once_with(
            key=settings.JWT_KEY_NAME, value="mock_token", httponly=True, max_age=settings.JWT_EXPIRES
        )


class TestRevokeTokenCookie:
    def test_revoke_token_cookie(self, mock_response):
        revoke_token_cookie(mock_response)
        mock_response.delete_cookie.assert_called_once_with(key=settings.JWT_KEY_NAME)


class TestGetCurrentUser:
    def test_get_current_user(self):
        token = create_token(DATA)
        user_id = get_current_user(token)
        assert user_id == "1"


class TestAuthenticateUser:
    def test_authenticate_user(self):
        provided_password = "test_password"
        hashed_password = hash_password(provided_password)
        authenticate_user(provided_password, hashed_password)

    def test_authenticate_user_invalid_password(self):
        provided_password = "incorrect_password"
        hashed_password = hash_password("correct_password")
        with pytest.raises(Unauthorized):
            authenticate_user(provided_password, hashed_password)


class TestVerifyPassword:
    def test_verify_password(self):
        plain_password = "test_password"
        hashed_password = hash_password(plain_password)
        result = verify_password(plain_password, hashed_password)
        assert result is True

    def test_verify_password_invalid(self):
        plain_password = "test_password"
        incorrect_password = "incorrect_password"
        hashed_password = hash_password(plain_password)
        result = verify_password(incorrect_password, hashed_password)
        assert result is False
