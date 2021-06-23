from services.client import ClientService
from utils.logging import logging

logger = logging.getLogger('onboarding')


def fill_risk_assessment(client):
    # Fill the risk assessment
    questions = ClientService.get_questions_for_risk_assessment(client)
    assessment_uuid = ClientService.fill_risk_assessment(client, questions)
    status, response = ClientService.complete_risk_assessment(client, assessment_uuid)
    assert status, response
    logger.info('Risk Assessment completed')
    return client
