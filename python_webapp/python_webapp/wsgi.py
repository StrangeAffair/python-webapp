"""
WSGI config for python_webapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application  # type: ignore # noqa: E501 # pylint: disable=E0401

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_webapp.settings')

application = get_wsgi_application()
