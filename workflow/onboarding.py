#!/usr/bin/env python
from faker import Faker
from services.client import ClientService
from services.integration_auth import IntegrationAuthService
from services.integration_client import ClientIntegrationService
from services.integration_portfolio import PortfolioIntegrationService
from utils.constants import COUNTRY_CODE_US
from utils.logging import logging

logger = logging.getLogger('onboarding')
faker = Faker('en_US')


def onboarding_client():
    """
        Create a client in ACTIVE status and a GIA Portfolio in ACTIVE status
    """
    access_token = IntegrationAuthService.login()

    # Create client using email and password
    status, client = ClientService.create(faker.email(), '.1234aaAAA')
    assert status, client
    logger.info('Client created')

    # Get information for the created client
    status, client = ClientService.me(client)
    assert status, client
    logger.info(f'Client me {client.email}')

    # Fill the profile information
    client_fields = {
        'first_name': faker.first_name(),
        'last_name': faker.last_name(),
        'phone_number': faker.phone_number().replace(' ', '')[:14],  # Phone number max 14
        'birthdate': faker.date_of_birth(minimum_age=20, maximum_age=100).strftime('%Y-%m-%d')
    }
    status, client = ClientService.patch_fields(client, **client_fields)
    assert status, f'{client} {client_fields}'
    logger.info(f'Client me {client.first_name} {client.last_name}')

    # Create an address for the client
    address_fields = {
        'line1': faker.street_address(),
        'postcode': faker.postcode(),
        'locality': faker.city(),
        'country': COUNTRY_CODE_US,
        'region': faker.administrative_unit()
    }
    status, client = ClientService.create_address(client, **address_fields)
    assert status, client
    logger.info(f'Client addresses: {client.addresses}')

    # Create a bank account for the client
    bank_account = {
        'iban': faker.iban()
    }
    status, client = ClientService.create_bank_accounts(client, **bank_account)
    assert status, client
    logger.info(f'Client bank accounts: {client.bank_accounts}')

    # Create tax information for the client
    tax_information = {
        'document_number': '11111',
        'country': 'GB',
        'document_type': 'NINO'
    }
    status, tx_information = ClientService.create_tax_information(client, **tax_information)
    assert status, tx_information
    logger.info(f'Client tax information: {tx_information}')

    # Start an Identity verification process
    status, verification = ClientService.create_kyc_identity(client)
    assert status, verification
    logger.info(f'KYC Identity Verification: {verification}')

    # Start a Bank verification process
    status, verification = ClientService.create_kyc_banking(client)
    assert status, verification
    logger.info(f'KYC Banking Verification: {verification}')

    # Attach information for Identity Verification
    status, verification = ClientService.verification_attach_document(client)
    assert status, verification
    logger.info('KYC Document Verification created')

    # Fill the risk assessment
    status, risk_assessment = ClientService.do_risk_assessment(client)
    assert status, risk_assessment
    logger.info('Risk Assessment completed')

    # Complete the onboarding
    status, completed_client = ClientService.complete_onborading(client)
    assert status, completed_client
    logger.info(f'Client {completed_client.status}')

    # Simulate the email verification process
    status, response_data = ClientIntegrationService.update_client(access_token, client, {'email_verified': True})
    assert status, response_data

    # Simulate identity verification process
    status, verification = ClientService.identity_verification_process(client)
    assert status, verification
    logger.info('KYC Identity Verification processed')

    # Simulate banking verification process
    status, verification = ClientService.banking_verification_process(client)
    assert status, verification
    logger.info('KYC Banking Verification processed')

    status, client = ClientService.me(client)
    assert status, client
    logger.info(f'Client me {client.status}')

    # Move client to ACTIVE, ready for operating
    status, response_data = ClientIntegrationService.update_client(access_token, client, {'status': 'ACTIVE'})
    assert status, response_data

    # Create a GIA portfolio
    status, client = ClientService.create_portfolio(client, name='My Portfolio')
    assert status, client
    portfolio = client.portfolios[0]

    # Active the portfolio for start operating.
    status, response_data = PortfolioIntegrationService.update_portfolio(access_token, portfolio, {'status': 'ACTIVE'})
    assert status, response_data

    status, client = ClientService.me(client)
    assert status, client
    logger.info(f'Client me {client.status}')


if __name__ == '__main__':
    onboarding_client()
