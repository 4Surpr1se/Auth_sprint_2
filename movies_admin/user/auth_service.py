import http
import json
from functools import lru_cache

import requests

from config import settings


# todo деградацию, rate limit
class AuthService:
    BASE_URL = settings.AUTHENTICATION_SERVICE_BASE_URL
    LOGIN_URL = settings.AUTHENTICATION_SERVICE_LOGIN_URL
    LOGOUT_URL = settings.AUTHENTICATION_SERVICE_LOGOUT_URL  # todo красиво
    REFRESH_URL = settings.AUTHENTICATION_SERVICE_REFRESH_URL  # todo красиво
    ME_URL = settings.AUTHENTICATION_SERVICE_ME_URL

    def login(self, username=None, password=None):
        payload = {'username': username, 'password': password}
        response = requests.post(self.LOGIN_URL, data=json.dumps(payload))
        return response.status_code, response.json()

    def logout(self):
        pass

    def refresh(self, refresh_token):
        payload = {
            "refresh_token": refresh_token
        }
        response = requests.post(self.REFRESH_URL, data=json.dumps(payload))
        return response.status_code, response.json()

    def me(self, access_token):
        response = requests.get(self.ME_URL,
                                headers={'Authorization': 'Bearer ' + access_token})
        return response.status_code, response.json()


@lru_cache
def get_auth_service() -> AuthService:
    return AuthService()
