from decouple import config

ENV_POSSIBLE_OPTIONS = (
    "local",
    "prod",
)
ENV_ID = config("DJANGORLAR_ENV_ID", cast=str)

SECRET_KEY = 'django-insecure-#@5#m*pf8et(yn0%)$3z&y=)euv0#srgjqb8a)*!6lk17om8dl'
