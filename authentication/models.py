from django.contrib.auth.models import AbstractUser
from django.db import models


class Try(models.Model):
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Try'
        verbose_name_plural = 'Tries'
