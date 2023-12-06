from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.contrib.auth.models import PermissionsMixin
from authentication.managers import UserManager
import string, random


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"


class ConfirmationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.code}"

    @staticmethod
    def generate_code():
        code_length = 4
        characters = string.digits
        return ''.join(random.choice(characters) for _ in range(code_length))
