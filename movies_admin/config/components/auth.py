import os

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = ["user.auth_backend.CustomBackend", ]

AUTHENTICATION_SERVICE_BASE_URL = os.environ.get('AUTHENTICATION_SERVICE_BASE_URL')
AUTHENTICATION_SERVICE_LOGIN_URL = os.environ.get('AUTHENTICATION_SERVICE_LOGIN_URL')
AUTHENTICATION_SERVICE_LOGOUT_URL = os.environ.get('AUTHENTICATION_SERVICE_LOGOUT_URL')
AUTHENTICATION_SERVICE_REFRESH_URL = os.environ.get('AUTHENTICATION_SERVICE_REFRESH_URL')
AUTHENTICATION_SERVICE_ME_URL = os.environ.get('AUTHENTICATION_SERVICE_ME_URL')

AUTH_USER_MODEL = "user.User"

DJANGO_ADMIN_LOGS_ENABLED = False  # todo переделать в идеале, чтобы он регал в базе просто айдишник через charfield
