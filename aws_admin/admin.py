from django.contrib import admin
from django.db.models import Count

from . import models


class InstanceCountMixin(object):
    def get_queryset(self, request):
        qs = super(InstanceCountMixin, self).get_queryset(request)
        return qs.annotate(instance_count=Count('instances'))

    def instance_count(self, obj):
        return obj.instance_count
    instance_count.short_description = 'Instances'


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.VPC)
class VPCAdmin(InstanceCountMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'cidr', 'state', 'instance_count')


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
class SecurityGroupAdmin(InstanceCountMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'vpc', 'description', 'instance_count')
    readonly_fields = ('tags', 'region', 'id', 'name', 'description', 'rules',
        'rules_egress', 'vpc')
    search_fields = ('id', 'name')
    # TODO how do I do an inline not to the through table?
    inlines = [InstanceInline]


@admin.register(models.SecurityGroupRule)
class SecurityGroupRuleAdmin(admin.ModelAdmin):
    list_display = ('protocol', 'port_range', 'cidr', 'source_group', 'description',
        'inbound')
    list_filter = ('protocol', )
    ordering = ('protocol', 'cidr')

    def get_queryset(self, request):
        qs = super(SecurityGroupRuleAdmin, self).get_queryset(request)
        return qs.annotate(inbound_count=Count('sgs_inbound'))

    def inbound(self, obj):
        return obj.inbound_count
