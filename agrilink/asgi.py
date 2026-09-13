"""
ASGI config for Agri Link project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agrilink.settings")
application = get_asgi_application()
