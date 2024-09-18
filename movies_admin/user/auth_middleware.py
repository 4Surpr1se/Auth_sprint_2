import http

from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from user.auth_service import get_auth_service
from user.auth_utils import _get_user_from_dict


def get_user(request):
    from django.contrib.auth.models import AnonymousUser
    auth_service = get_auth_service()
    access_token = request.COOKIES.get('access_token')
    if access_token:
        status_code, user_data = auth_service.me(access_token)
        if status_code == http.HTTPStatus.OK:
            return _get_user_from_dict(
                user_data)  # todo мб поменять базовый AbstractUser, чтобы сериализовалась по User модели, чтобы pydantic не подключать
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        status_code, refresh_data = auth_service.refresh(refresh_token)
        if status_code == http.HTTPStatus.OK:
            access_token = refresh_data['access_token']
            status_code, user_data = auth_service.me(access_token)
            if status_code == http.HTTPStatus.OK:
                return _get_user_from_dict(user_data)
    return AnonymousUser()


def get_user_cached(request):
    if not hasattr(request, "_cached_user"):
        request._cached_user = get_user(request)
    return request._cached_user


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user_cached(request))
