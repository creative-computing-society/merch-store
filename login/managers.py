from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
class UserManager(BaseUserManager):
    """
    Custom User Manager to use email as unique identifier
    """

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email required")

        user = self.model(
            email=email,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user