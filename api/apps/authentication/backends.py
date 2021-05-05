from django.conf import settings

from accounts.models import User

import inspect


def get_request():
    for f in inspect.stack():
        f_code = inspect.getmembers(f.frame, inspect.iscode)[0][1]
        f_locals = [v for (n, v) in inspect.getmembers(f.frame) if n == "f_locals"][0]
        co_varnames = [v for (n, v) in inspect.getmembers(f_code) if n == "co_varnames"][0]
        if "request" in co_varnames:
            return f_locals["request"]


class AuthByDbBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username__iexact=username)
        except:
            return None
        if not user.check_password(password):
            return None
        return user

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)
