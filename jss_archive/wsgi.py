# WSGI config for jss_archive project.
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jss_archive.settings')
application = get_wsgi_application()
app = application

