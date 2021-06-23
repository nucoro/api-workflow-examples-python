from faker import Faker
from services.client import ClientService
from utils.logging import logging

logger = logging.getLogger('onboarding')
faker = Faker('en_US')


def run_kyc_aml(client):
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
    return client


def complete_verifications(client):
    # Simulate identity verification process
    status, verification = ClientService.identity_verification_process(client)
    assert status, verification
    logger.info('KYC Identity Verification processed')

    # Simulate banking verification process
    status, verification = ClientService.banking_verification_process(client)
    assert status, verification
    logger.info('KYC Banking Verification processed')
    return client
