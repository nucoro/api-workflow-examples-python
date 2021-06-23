# Nucoro developer account backend

## Instructions for installing

- pipenv shell
- pipenv install
- pipenv install --dev (if local)
- Create .env file using .env.dist

### Configuration file

You have to configure these variables inside .env file:
- BASE_URL: this is the URL for your sandbox deploy.
- CLIENT_USER: client email if you want to operate as a client
- CLIENT_PASSWORD: client password if you want to operate as a client
- CLIENT_ID: this is only for the integration API, the client ID defined for your OAuth application
- CLIENT_SECRET: this is only for the integration API, the client secret defined for your OAuth application
- KID: this is only for the integration API, the KID defined for your OAuth application

## Workflows

### Onboarding
This example shows how to create a client using the API. You can see two different ways for creating a client.

- Execute `python -m workflow.onboarding`
