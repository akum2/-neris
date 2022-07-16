from django.contrib import admin
from django.contrib.auth.models import Group, User

from authentication.models import *

admin.site.register(UploadedDocuments)
admin.site.register(TheUsers)
