from pathlib import Path
import os
import django_heroku
import environ as django_environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.contrib import messages

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
env = django_environ.Env()
django_environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = [
    'https://uba-plagio.herokuapp.com/',
    'https://www.uba-plagio.herokuapp.com/',
    'uba-plagio.herokuapp.com/',
    '127.0.0.1',
    'localhost',
]

# Application definition

INSTALLED_APPS = [
    'authentication',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_heroku',
    'user_visit',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'user_visit.middleware.UserVisitMiddleware',
]

django_heroku.settings(locals())

ROOT_URLCONF = 'plagiarism.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'plagiarism.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PORT': env('DB_PORT'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Douala'

USE_I18N = True

USE_TZ = True

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# Amazon config
AWS_LOCATION = 'static'
AWS_STORAGE_BUCKET_NAME = 'plagio-store'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.eu-west-3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = True
DEFAULT_FILE_STORAGE = 'authentication.storage_backends.MediaStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

# Login SYSTEM
LOGIN_URL = 'signin'
LOGIN_REDIRECT_URL = 'signin'
AUTH_USER_MODEL = 'authentication.TheUsers'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
AWS_LOCATION_MEDIA = 'media'
MEDIA_ROOT = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION_MEDIA)
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION_MEDIA)

LOGOUT_REDIRECT_URL = 'signin'
