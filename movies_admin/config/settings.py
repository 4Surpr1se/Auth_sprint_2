import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent

# todo makemigrations сделать
load_dotenv(find_dotenv('example.env'))

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', False) == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

INTERNAL_IPS = [
    "127.0.0.1",
]

include('components/installed_apps.py')

include('components/middleware.py')

ROOT_URLCONF = 'config.urls'

include('components/templates.py')

WSGI_APPLICATION = 'config.wsgi.application'

include(
    'components/database.py',
)


include('components/auth.py')


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

LOCALE_PATHS = ['movies/locale']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

ENABLE_STACKTRACES = True
