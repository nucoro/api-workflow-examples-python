import requests
from utils.resolver import reverse


class ClientIntegrationService():

    @classmethod
    def update_client(cls, token, client, data):
        """
            Update the client information
        """
        url = reverse('integration-client-detail', uuid=str(client.uuid))
        response = requests.patch(
            url,
            headers={'Authorization': f'Bearer {token}'},
            data=data
        )
        return response.ok, response.json()
