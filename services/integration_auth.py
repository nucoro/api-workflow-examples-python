import os
from exceptions import AuthNotAllowed

import requests
from utils.constants import INTEGRATION_AUTH_TOKEN_URL
from utils.jwt import generate_basic_token, generate_personal_jwt


class IntegrationAuthService:
    _token = None

    @classmethod
    def login(cls):
        """
            Obtain access token for oauth
        """
        client_id = os.environ.get('CLIENT_ID')
        base_url = os.environ.get('BASE_URL')
        kid = os.environ.get('KID')
        header = generate_basic_token()
        private_key = ''
        with open('private_key.pem', 'r') as f:
            private_key = f.read()
        assertion = generate_personal_jwt(client_id, private_key.encode('utf-8'), kid, None)
        data = {
            'grant_type': 'urn:nucoro:oauth:grant-type:jwt',
            'assertion': assertion,
        }

        response = requests.post(
            f'{base_url}{INTEGRATION_AUTH_TOKEN_URL}',
            headers={'Authorization': f'Basic {header}'},
            data=data)
        if response.ok:
            cls._token = response.json().get('access_token')
            return cls._token
        else:
            raise AuthNotAllowed('Access not allowed')
