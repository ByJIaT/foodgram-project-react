import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        email='admin@foodgram.fake',
        username='admin',
        first_name='admin',
        last_name='admin',
        password='qwerty1234',
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        email='user@foodgram.fake',
        username='user',
        first_name='user',
        last_name='user',
        password='qwerty1234',
    )


@pytest.fixture
def token_admin(admin):
    token = AccessToken.for_user(admin)
    return {
        'access': str(token)
    }


@pytest.fixture
def admin_client(token_admin):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_admin["access"]}')
    return client


@pytest.fixture
def token_user(user):
    token = AccessToken.for_user(user)
    return {
        'access': str(token)
    }


@pytest.fixture
def user_client(token_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_user["access"]}')
    return client
