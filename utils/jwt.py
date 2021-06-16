import base64
import os

from authlib.jose import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def generate_basic_token():
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    return base64.b64encode(str.encode(f'{CLIENT_ID}:{CLIENT_SECRET}')).decode('utf-8')


def generate_personal_jwt(client_id, private_key, kid, password):

    private_key = serialization.load_pem_private_key(private_key, password=password, backend=default_backend())

    payload = {
        'aud': '/oauth/token/',
        'iss': client_id,
        'exp': 1700249022,
    }

    headers = {'alg': 'RS256', 'kid': kid}

    return jwt.encode(headers, payload, private_key).decode('utf-8')
