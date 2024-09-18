import os
from dotenv import load_dotenv

from config import settings

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'movies.apps.MoviesConfig',
    'user.apps.UserConfig',
    'django_admin_logs',
]
if settings.DEBUG:
    load_dotenv()
    INSTALLED_APPS.append('debug_toolbar')
