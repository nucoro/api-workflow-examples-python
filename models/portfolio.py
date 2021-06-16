from .base import BaseModel


class Portfolio(BaseModel):

    def __str__(self):
        return self.name
