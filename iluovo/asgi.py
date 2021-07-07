"""
ASGI config for iluovo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iluovo.settings')

application = get_asgi_application()

import newrelic.agent
newrelic.agent.initialize(os.path.join(os.path.dirname(__file__), "newrelic.ini"))
application = newrelic.agent.asgi_application(application)