import requests
from utils.resolver import reverse


class PortfolioIntegrationService():

    @classmethod
    def update_portfolio(cls, token, portfolio, data):
        """
            Update the portfolio information
        """
        url = reverse('integration-portfolio-detail', uuid=str(portfolio.uuid))
        response = requests.patch(
            url,
            headers={'Authorization': f'Bearer {token}'},
            data=data
        )
        return response.ok, response.json()
