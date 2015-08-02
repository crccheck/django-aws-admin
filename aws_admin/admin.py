from django.contrib import admin
from django.db.models import Count

from . import models


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.VPC)
class VPCAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cidr', 'state')


@admin.register(models.Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'state', 'vpc', 'launched')
    list_filter = ('region', 'state')
    readonly_fields = ('id', 'region', 'name', 'state', 'data', 'launched',
        'security_groups', 'tags', 'vpc')


class InstanceInline(admin.TabularInline):
    model = models.Instance.security_groups.through
    extra = 0


@admin.register(models.SecurityGroup)
class SecurityGroupAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(SecurityGroupAdmin, self).get_queryset(request)
        return qs.annotate(instance_count=Count('instances'))

    def instance_count(self, obj):
        return obj.instance_count
    instance_count.short_description = 'Instances'

    list_display = ('id', 'name', 'vpc', 'description', 'instance_count')
    readonly_fields = ('tags', 'region', 'id', 'name', 'description', 'rules',
        'rules_egress', 'vpc')
    search_fields = ('id', 'name')
    # TODO how do I do an inline not to the through table?
    inlines = [InstanceInline]
