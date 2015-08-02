from django.contrib import admin

from . import models


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'state', 'launched')
    list_filter = ('region', 'state')
    readonly_fields = ('id', 'region', 'name', 'state', 'data', 'launched',
        'security_groups', 'tags')


@admin.register(models.SecurityGroup)
class SecurityGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'vpc', 'description')
    readonly_fields = ('tags', 'region', 'id', 'name', 'description', 'rules',
        'rules_egress', 'vpc')
