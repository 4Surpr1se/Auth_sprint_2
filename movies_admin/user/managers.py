from django.contrib.auth.base_user import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, id, username, email, password=None, **kwargs):
        user = self.model(id=id, username=username, email=email)
        if not kwargs.get('first_name') and not kwargs.get('last_name'):
            user.first_name = username
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, username, email, password=None, **kwargs):
        user = self.create_user(id, username, email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
