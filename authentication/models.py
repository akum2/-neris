from tabnanny import verbose
from django.contrib.auth.models import AbstractUser
from django.db import models


class Try(models.Model):
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Try'
        verbose_name_plural = 'Tries'

class Check(models.Model):
    added_on = models.DateTimeField(auto_now=True, verbose_name="Added Date")
    document_title = models.CharField(max_length=75, verbose_name="Documet Title")
    author = models.CharField(verbose_name="Author", max_length=30)
    document_content = models.CharField(max_length=12000000000000, unique=False, verbose_name="Document Content")

    def __str__(self):
        return self.document_title
