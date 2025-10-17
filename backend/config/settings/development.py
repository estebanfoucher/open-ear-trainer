"""
Development settings for the ear trainer project.
"""

from .base import *

# Override for development
DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]

# Development-specific CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# Disable cache in development
AUDIO_CACHE_ENABLED = False

# Development logging
LOGGING["handlers"]["console"]["level"] = "DEBUG"
LOGGING["root"]["level"] = "DEBUG"
