from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=9,primary_key=True) 
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_no = models.CharField(max_length=15, null=True, default=None, blank=True)
    name = models.CharField(max_length=100, null=True, default=None, blank=True)
    position = models.CharField(max_length=10, default='user')
    profilePic = models.URLField(max_length=500, null=True, blank=True, default=None)


    is_member = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
