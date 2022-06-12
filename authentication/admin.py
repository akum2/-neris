from django.contrib import admin
from django.contrib.auth.models import Group, User

from authentication.models import *

admin.site.register(Try)
admin.site.register(Check)
admin.site.register(TheUsers)
