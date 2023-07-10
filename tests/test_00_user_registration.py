import pytest
from rest_framework import status


@pytest.mark.django_db(transaction=True)
class Test00UserRegistration:
    url_signup = '/api/users/'
    url_token = '/api/auth/token/login/'

    def test_00_no_data_signup(self, client, django_user_model):
        response = client.post(self.url_signup, data={})

    def test_00_invalid_data_signup(self, client, django_user_model):
        ...

    def test_00_valid_data_signup(self, client, django_user_model):
        valid_data = {
            'email': 'valid@foodgram.fake',
            'username': 'valid_username',
            'first_name': 'valid_user',
            'last_name': 'valid_user',
            'password': 'dafgEjdl342',
        }

        response = client.post(self.url_signup, data=valid_data)

        assert response.status_code == status.HTTP_201_CREATED
