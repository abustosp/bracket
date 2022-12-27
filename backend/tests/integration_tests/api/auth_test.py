from contextlib import contextmanager
from typing import Generator
from unittest.mock import Mock, patch

import jwt

from bracket.config import config
from bracket.utils.http import HTTPMethod
from bracket.utils.types import JsonDict
from tests.integration_tests.api.shared import send_request
from tests.integration_tests.mocks import MOCK_NOW, MOCK_USER, get_mock_token
from tests.integration_tests.sql import inserted_user


@contextmanager
def mock_auth_time() -> Generator[None, None, None]:
    with patch('bracket.routes.auth.datetime_utc.now', Mock(return_value=MOCK_NOW)):
        yield


async def test_get_token_success(startup_and_shutdown_uvicorn_server: None) -> None:
    body = {
        'username': MOCK_USER.email,
        'password': 'mypassword',
    }
    with mock_auth_time():
        async with inserted_user(MOCK_USER):
            response = JsonDict(await send_request(HTTPMethod.POST, 'token', body))

    assert 'access_token' in response
    assert response.get('token_type') == 'bearer'

    decoded = jwt.decode(response['access_token'], config.jwt_secret, algorithms=['HS256'])
    assert decoded == {'user': MOCK_USER.email, 'exp': 7258723200}


async def test_get_token_invalid_credentials(startup_and_shutdown_uvicorn_server: None) -> None:
    body = {
        'username': MOCK_USER.email,
        'password': 'invalid password',
    }
    with mock_auth_time():
        async with inserted_user(MOCK_USER):
            response = JsonDict(await send_request(HTTPMethod.POST, 'token', body))

    assert response == {'detail': 'Incorrect email or password'}


async def test_auth_on_protected_endpoint(startup_and_shutdown_uvicorn_server: None) -> None:
    headers = {'Authorization': f'Bearer {get_mock_token()}'}

    async with inserted_user(MOCK_USER) as user_inserted:
        response = JsonDict(await send_request(HTTPMethod.GET, 'users/me', {}, headers))

        assert response == {
            'id': user_inserted.id,
            'email': user_inserted.email,
            'name': user_inserted.name,
            'created': '2200-01-01T00:00:00+00:00',
        }


async def test_invalid_token(startup_and_shutdown_uvicorn_server: None) -> None:
    headers = {'Authorization': 'Bearer some.invalid.token'}

    response = JsonDict(await send_request(HTTPMethod.GET, 'users/me', {}, headers))
    assert response == {'detail': 'Could not validate credentials'}
