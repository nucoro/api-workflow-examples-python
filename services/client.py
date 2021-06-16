import random

import requests
from models import Address, BankAccount, Client, Portfolio
from utils.images import generate_fake_image
from utils.resolver import reverse


class ClientService:

    @classmethod
    def create(cls, email, password):
        """
            Create a client using only email and password
        """
        url = reverse('client-create')
        payload = {
            'email': email,
            'password': password
        }

        response = requests.post(url, json=payload)
        if response.ok:
            data = response.json()
            access = data.pop('access')
            refresh = data.pop('refresh')
            client = Client(**data)
            client.set_token(access, refresh)
            return True, client
        else:
            return False, response.json()

    @classmethod
    def me(cls, client):
        """
            Get client info
        """
        assert client._token, 'user not authenticated'
        url = reverse('client-me')
        response = requests.get(url, headers={'Authorization': client._token.get('access')})
        if response.ok:
            client.update(**response.json())
            return True, client
        else:
            return False, response.json()

    @classmethod
    def patch_fields(cls, client, **kwargs):
        """
            Update some fields for a client
        """
        assert client._token, 'user not authenticated'
        url = reverse('client-me')
        response = requests.patch(url, json=kwargs, headers={'Authorization': client._token.get('access')})
        if response.ok:
            client.update(**response.json())
            return True, client
        else:
            return False, response.json()

    @classmethod
    def addresses(cls, client):
        """
            Get addresses for a client
        """
        assert client._token, 'user not authenticated'
        url = reverse('client-addresses')
        response = requests.get(url, headers={'Authorization': client._token.get('access')})
        if response.ok:
            client.addresses = [Address(**data) for data in response.json()['results']]
            return True, client
        else:
            return False, response.json()

    @classmethod
    def create_address(cls, client, **kwargs):
        """
            Create a new address for the client
        """
        assert client._token, 'user not authenticated'
        url = reverse('client-addresses')
        response = requests.post(url, json=kwargs, headers={'Authorization': client._token.get('access')})
        if response.ok:
            client.addresses.append(Address(**response.json()))
            return True, client
        else:
            return False, response.json()

    @classmethod
    def create_bank_accounts(cls, client, **kwargs):
        """
            Create a bank account for the client
        """
        assert client._token, 'user not authenticated'
        url = reverse('client-bank-accounts')
        response = requests.post(url, json=kwargs, headers={'Authorization': client._token.get('access')})
        if response.ok:
            client.bank_accounts.append(BankAccount(**response.json()))
            return True, client
        else:
            return False, response.json()

    @classmethod
    def create_tax_information(cls, client, **kwargs):
        """
            Create tax information fot the client
        """
        assert client._token, 'user not authenticated'
        url = reverse('client-tax-information')
        response = requests.post(url, json=kwargs, headers={'Authorization': client._token.get('access')})
        return response.ok, response.json()

    @classmethod
    def create_kyc_identity(cls, client):
        """
            Create an Identity Verification for the client
        """
        assert client._token, 'user not authenticated'
        url = reverse('client-kyc-identity')
        response = requests.post(url, headers={'Authorization': client._token.get('access')})
        return response.ok, response.json()

    @classmethod
    def create_kyc_banking(cls, client):
        """
            Create a Banking Verification for the client
        """
        assert client._token, 'user not authenticated'
        url = reverse('client-kyc-banking')
        response = requests.post(url, headers={'Authorization': client._token.get('access')})
        return response.ok, response.json()

    @classmethod
    def verification_attach_document(cls, client):
        """
            Attach a document for the identity verification
        """
        url = reverse('client-kyc-identity-attach')
        response = requests.post(
            url,
            headers={'Authorization': client._token.get('access')},
            data={'document_type': 'passport'},
            files={
                'front': generate_fake_image(),
                'back': generate_fake_image()
            })
        return response.ok, response.json()

    @classmethod
    def identity_verification_process(cls, client):
        """
            Process the last identity verification for the client
        """
        url = reverse('client-kyc-identity-process')
        response = requests.post(url, headers={'Authorization': client._token.get('access')})
        return response.ok, response.json()

    @classmethod
    def banking_verification_process(cls, client):
        """
            Process the last banking verification for the client
        """
        url = reverse('client-kyc-banking-process')
        response = requests.post(url, headers={'Authorization': client._token.get('access')})
        return response.ok, response.json()

    @classmethod
    def do_risk_assessment(cls, client):
        """
            Fill the risk assessment for the client
        """
        url = reverse('risk-questions')
        response = requests.get(url, headers={'Authorization': client._token.get('access')})
        assert response.ok
        data = [random.choice(data['choices'])['code'] for data in response.json()['results']]

        # Create the assessment for the user
        url = reverse('client-fill-risk-assessment')
        response = requests.post(url, json={'choices': data}, headers={'Authorization': client._token.get('access')})
        assert response.ok
        assessment_uuid = response.json()['uuid']

        # Complete the assessment
        url = reverse('client-complete-risk-assessment', uuid=assessment_uuid)
        response = requests.post(url, headers={'Authorization': client._token.get('access')})
        return response.ok, response.json()

    @classmethod
    def complete_onborading(cls, client):
        """
            Complete the onboarding for the client and move the status
        """
        url = reverse('client-complete-onboarding')
        response = requests.post(url, headers={'Authorization': client._token.get('access')})
        if response.ok:
            client.update(**response.json())
            return True, client
        else:
            return False, response.json()

    @classmethod
    def create_portfolio(cls, client, name):
        """
            Create a GIA Portfolio for the client
        """
        url = reverse('client-portfolio-create')
        data = {
            'name': name,
            'portfolio_type': 'GIA'
        }
        response = requests.post(url, headers={'Authorization': client._token.get('access')}, data=data)
        if response.ok:
            portfolio = Portfolio(**response.json())
            client.portfolios.append(portfolio)
            return True, client
        else:
            return False, response.json()
