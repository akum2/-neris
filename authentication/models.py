from django.contrib.auth.models import AbstractUser
from django.db import models


class Try(models.Model):
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Try'
        verbose_name_plural = 'Tries'


class Login(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Login'
        verbose_name_plural = 'Logins'

    def __str__(self):
        return self.username
