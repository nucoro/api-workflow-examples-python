from .base import BaseModel


class Client(BaseModel):
    _token = {}
    addresses = []
    bank_accounts = []
    portfolios = []

    def set_token(self, access, refresh):
        self._token = {
            'access': access,
            'refresh': refresh
        }

    def __str__(self):
        return self.email
