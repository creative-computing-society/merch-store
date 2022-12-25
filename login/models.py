from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


USER_POSITION_CHOICES = [
    ('MB','Member'),
    ('CR','Core'),
    ('JS','Joint Secretary'),
    ('GS','General Secretary'),
]

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15, null=True, default=None, blank=True)
    name = models.CharField(max_length=100, null=True, default=None, blank=True)
    position = models.CharField(max_length=2, choices=USER_POSITION_CHOICES, default='MB')
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def get_short_name(self):
        # The user is identified by their email
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
           return True
    
    def __str__(self):
        return self.email
    

    
