from faker import Faker
from services.client import ClientService
from utils.constants import COUNTRY_CODE_US
from utils.logging import logging

logger = logging.getLogger('onboarding')
faker = Faker('en_US')


def create_client_and_profile():
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
    return client


def complete_onboarding(client):
    # Complete the onboarding
    status, completed_client = ClientService.complete_onborading(client)
    assert status, completed_client
    logger.info(f'Client {completed_client.status}')
    return client
