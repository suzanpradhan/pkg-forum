from django.contrib import admin


from .models import Package, PackageSocial, Registry

admin.site.register(Registry)
admin.site.register(PackageSocial)
admin.site.register(Package)
