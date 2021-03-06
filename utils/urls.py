urls_pattern = {
    'application-login': '/auth/login/',
    'client-create': '/clients/',
    'client-me': '/clients/me/',
    'client-addresses': '/clients/me/addresses/',
    'client-bank-accounts': '/clients/me/bank-accounts/',
    'client-tax-information': '/clients/me/tax-informations/',
    'client-kyc-identity': '/clients/me/verifications/identity/',
    'client-kyc-identity-attach': '/clients/me/verifications/identity/documents/',
    'client-kyc-identity-process': '/clients/me/verifications/identity/latest/process/',
    'client-kyc-banking': '/clients/me/verifications/banking/',
    'client-kyc-banking-process': '/clients/me/verifications/banking/latest/process/',
    'risk-questions': '/risk/questions/',
    'client-fill-risk-assessment': '/clients/me/risk-assessments/',
    'client-complete-risk-assessment': '/clients/me/risk-assessments/{uuid}/complete/',
    'client-complete-onboarding': '/clients/me/onboarding/complete/',
    'client-portfolio-create': '/portfolios/',
    'integration-client-detail': '/integration/account/clients/{uuid}/',
    'integration-portfolio-detail': '/integration/portfolios/{uuid}/',
}
