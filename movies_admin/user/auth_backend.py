import http

from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth import get_user_model, user_logged_in
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.middleware.csrf import rotate_token

from user.auth_service import get_auth_service
from user.auth_utils import _get_user_from_dict

User = get_user_model()


class CustomBackend(BaseBackend):

    def __init__(self):
        self.auth_service = get_auth_service()

    def authenticate(self, request, username=None, password=None):
        status_code, data = self.auth_service.login(username, password)
        if status_code != http.HTTPStatus.OK:
            return None
        status_code, response_for_data = self.auth_service.me(data.get('access_token'))
        try:
            user = _get_user_from_dict(response_for_data)
            user.access_token = data.get('access_token')
            user.refresh_token = data.get('refresh_token')
        except:
            return None
        return user


class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'  # Customize the login template if needed
    next_page = 'admin:index'

    def form_valid(self, form):
        user = self.login(form)
        self.request.user = user
        rotate_token(self.request)
        response = HttpResponseRedirect(self.get_success_url())
        response.set_cookie('access_token', user.access_token)
        response.set_cookie('refresh_token', user.refresh_token)
        user_logged_in.send(sender=user.__class__, request=self.request, user=user)
        return response

    def login(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        return authenticate(self.request, username=username, password=password)


def admin_logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response
