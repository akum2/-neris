from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models


class TheUserManager(BaseUserManager):
    # defining a function or method that will create user
    def create_user(self, username, email, name, phone, password):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError('Email is required')
        if not phone:
            raise ValueError('An appropriate phone number is required')
        if not name:
            raise ValueError("Enter your correct names")

        user = self.model(
            username=username,
            email=email,
            phone=phone,
            name=name,
            password=password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Creating our superuser
    def create_superuser(self, username, email, phone, name, password):
        user = self.create_user(
            username=username,
            email=email,
            phone=phone,
            password=password,
            name=name
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class TheUsers(AbstractBaseUser):
    username = models.CharField(
        verbose_name='Username',
        max_length=60,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=60,
        unique=True
    )
    name = models.CharField(
        verbose_name='Full Name',
        max_length=200,
        unique=True
    )
    phone = models.CharField(
        verbose_name="Phone Number",
        max_length=20, null=False
    )
    date_joined = models.DateTimeField(
        verbose_name='Created On',
        auto_now_add=True
    )
    profile = models.ImageField(
        verbose_name='Picture',
        upload_to=f'profiles/%Y/',
        default='profiles/unknown_user.png',
        null=False
    )
    last_login = models.DateTimeField(
        verbose_name='Last login',
        auto_now=True,
        null=False
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # Fields to log in to app
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'phone', 'email']

    def __str__(self):
        return self.username

    objects = TheUserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        verbose_name = "User"
        verbose_name_plural = 'Users'


class Try(models.Model):
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Try'
        verbose_name_plural = 'Tries'


class Check(models.Model):
    added_on = models.DateTimeField(auto_now=True, verbose_name="Added Date")
    document_title = models.CharField(max_length=75, verbose_name="Document Title")
    author = models.CharField(verbose_name="Author", max_length=30)
    document_content = models.CharField(max_length=12000, unique=False, verbose_name="Document Content")

    def __str__(self):
        return self.document_title
