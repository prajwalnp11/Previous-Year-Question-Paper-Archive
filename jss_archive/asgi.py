# ASGI config for jss_archive project.
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jss_archive.settings')
application = get_asgi_application()
