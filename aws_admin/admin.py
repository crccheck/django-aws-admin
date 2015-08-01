from django.contrib import admin

from . import models


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'state', 'launched')
    list_filter = ('region', 'state')
