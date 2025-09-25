#Python modules
from decouple import config

ENV_POSSIBLE_OPTIONS=(
    "prod",
    "local",
)

ENV_ID=config("DJANGORLAR_ENV_ID", cast=str)
SECRET_KEY = 'django-insecure-v1ylp#4jjx76hl9g++2ae4syt!soc+z-#f-1o=s9i*swpqv=hl'
