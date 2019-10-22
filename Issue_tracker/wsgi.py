"""
WSGI config for Issue_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

path = 'home/baliks/django_backend_for_gde_issue_tracker'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'Issue_tracker.settings'

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()





# """
# WSGI config for Issue_tracker project.

# It exposes the WSGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
# """

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Issue_tracker.settings")

# application = get_wsgi_application()
