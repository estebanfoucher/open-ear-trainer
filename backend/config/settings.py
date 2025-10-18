"""
Django settings for config project.
"""

from decouple import config

# Import the appropriate settings based on environment
DJANGO_SETTINGS_MODULE = config(
    "DJANGO_SETTINGS_MODULE", default="config.settings.development"
)

if DJANGO_SETTINGS_MODULE == "config.settings.development":
    from .development import *
elif DJANGO_SETTINGS_MODULE == "config.settings.test":
    from .test import *
else:
    from .base import *
