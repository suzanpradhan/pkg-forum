from django.contrib import admin
from django.contrib.auth.models import Permission

from src.core.models import AccessSupport

admin.site.register(Permission)
admin.site.register(AccessSupport)
