from django.contrib import admin
from django.contrib.auth.models import Group, User

from authentication.models import Try

admin.site.register(Try)
# admin.site.unregister(User)
# admin.site.unregister(Group)
