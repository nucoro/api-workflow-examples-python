from .base import BaseModel


class Address(BaseModel):

    def __str__(self):
        return f'{self.line1}, {self.postcode} - {self.locality}'
