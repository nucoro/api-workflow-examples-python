# Nucoro API workflow examples with Python
This is a collection of different workflows using the Nucoro APIs with Python.

### Workflow examples included:
* Onboarding and activating a client using the Client API and Integration API. Execute `python -m workflow.onboarding`

# Requirements
You need a Nucoro sandbox environment to run the workflows. If you don't have Nucoro Sandbox Environment you can apply for a Developer Account in our [Developer Portal](https://developer.nucoro.com/). With a Developer Account you will be able to launch a Nucoro Sandbox Environment.

# Instructions

- pipenv shell
- pipenv install
- pipenv install --dev (if local)
- Create .env file using .env.dist

## Configuration file

You have to configure these variables inside .env file:
- BASE_URL: this is the URL for your sandbox deploy.
- CLIENT_USER: client email if you want to operate as a client
- CLIENT_PASSWORD: client password if you want to operate as a client
- CLIENT_ID: this is only for the integration API, the client ID defined for your OAuth application
- CLIENT_SECRET: this is only for the integration API, the client secret defined for your OAuth application
- KID: this is only for the integration API, the KID defined for your OAuth application
