import hashlib
from django.contrib.auth.backends import BaseBackend
from .models import User


class MD5Backend(BaseBackend):      # MD5密码的认证后端

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        # 使用MD5验证密码
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None