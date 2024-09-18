import os
from dotenv import load_dotenv

from config import settings
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user.auth_middleware.AuthenticationMiddleware'
]

if settings.DEBUG:
    load_dotenv()
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")