#!/usr/bin/env python
from faker import Faker
from services.client import ClientService
from services.integration_auth import IntegrationAuthService
from services.integration_client import ClientIntegrationService
from services.integration_portfolio import PortfolioIntegrationService
from utils.logging import logging
from workflow.modules import client as client_module
from workflow.modules import kyc_aml as kyc_aml_module
from workflow.modules import portfolio as portfolio_module
from workflow.modules import risk as risk_module

logger = logging.getLogger('onboarding')
faker = Faker('en_US')


def onboarding_client_self_trading():
    """
        Create a client for self trading.
        This client should be in ACTIVE status and having a GIA Portfolio in ACTIVE status
    """
    access_token = IntegrationAuthService.login()

    client = client_module.create_client_and_profile()
    client = kyc_aml_module.run_kyc_aml(client)
    client = risk_module.fill_risk_assessment(client)
    client = client_module.complete_onboarding(client)

    # Simulate the email verification process
    status, response_data = ClientIntegrationService.update_client(access_token, client, {'email_verified': True})
    assert status, response_data

    client = kyc_aml_module.complete_verifications(client)

    # Move client to ACTIVE, ready for operating
    status, response_data = ClientIntegrationService.update_client(access_token, client, {'status': 'ACTIVE'})
    assert status, response_data

    portfolio = portfolio_module.create_portfolio(client)

    # Active the portfolio for start operating.
    status, response_data = PortfolioIntegrationService.update_portfolio(access_token, portfolio, {'status': 'ACTIVE'})
    assert status, response_data

    status, client = ClientService.me(client)
    assert status, client
    logger.info(f'Client me {client.status}')


def onboarding_client_robo_advisor():
    """
        Create a client for robo advisor.
        This client should be in KYC_PENDING status and having a GIA Portfolio in PENDING status
    """
    client = client_module.create_client_and_profile()
    client = kyc_aml_module.run_kyc_aml(client)
    client = risk_module.fill_risk_assessment(client)
    client = client_module.complete_onboarding(client)
    portfolio = portfolio_module.create_portfolio(client)
    logger.info(f'Portfolio created: {portfolio} ({portfolio.status})')

    status, client = ClientService.me(client)
    assert status, client
    logger.info(f'Client me {client.status}')


if __name__ == '__main__':
    onboarding_client_self_trading()
    onboarding_client_robo_advisor()
