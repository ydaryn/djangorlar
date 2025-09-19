#Project mocules
from decouple import config

#ENV ID
ENV_POSSIBLE_OPTIONS=(
    'local',
    'prod',
)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m5$(8eg^5odruuc&y3n88k!b#04en#u96@-tu&h#)gjd)1wh3#'
ENV_ID = config("DJANGORLAR_ENV_ID", cast=str)