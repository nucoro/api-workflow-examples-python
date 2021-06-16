from .base import BaseModel


class BankAccount(BaseModel):

    def __str__(self):
        return self.account_number or self.iban
