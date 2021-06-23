from services.client import ClientService
from utils.logging import logging

logger = logging.getLogger('onboarding')


def create_portfolio(client):
    # Create a GIA portfolio
    status, client = ClientService.create_portfolio(client, name='My Portfolio')
    assert status, client
    portfolio = client.portfolios[0]
    return portfolio
