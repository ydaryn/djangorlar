#Python modules
import os

#Project modules
from settings.conf import ENV_ID, ENV_POSSIBLE_OPTIONS

#DJANGO modules
from django.core.asgi import get_asgi_application

if ENV_ID not in ENV_POSSIBLE_OPTIONS:
    raise ValueError(f"Invalid env id. Possible option: {ENV_POSSIBLE_OPTIONS}")
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.env.{ENV_ID}')
    
application = get_asgi_application()
