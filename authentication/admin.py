from django.contrib import admin
from django.contrib.auth.models import Group, User

from authentication.models import Try

admin.site.register(Try)
