import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from user.managers import MyUserManager


class User(AbstractBaseUser):
    # Из-за того, что я решил миддлвейр переписывать, там много оказалось методов и полей, которые тоже нужно реализовывать,
    # Но сроки поджимают, поэтому пока без ролей и пермишенов

    # Так же если получится оценить админку в муви, будет круто, потому что у меня дошли руки ее переписать,
    # по факту там тоже есть дыры, но общая реализация видна,
    # без нее очень много лишних запросов происходило
    # todo чтобы параметры полей откуда-то доставались
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'username'

    objects = MyUserManager()

    def __str__(self):
        return f'{self.email} {self.id}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        pass

    def has_usable_password(self, pas):
        return True

    def set_password(self, raw_password):
        pass
