import os
from exceptions import AuthNotAllowed

import requests
from utils.resolver import reverse


class AuthService:
    _token = {}

    def login(self):
        username = os.environ.get('CLIENT_USER')
        password = os.environ.get('CLIENT_PASS')
        url = reverse('application-login')
        response = requests.post(url, json={
            'username': username,
            'password': password
        })
        if response.ok:
            self._token = response.json()
        else:
            raise AuthNotAllowed('username/password incorrect')
