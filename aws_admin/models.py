from __future__ import unicode_literals

from django.db import models
from django_extensions.db.fields.json import JSONField


class Region(models.Model):
    code = models.SlugField(max_length=30, unique=True)
    name = models.CharField(max_length=55)

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.code)


class VPC(models.Model):
    """WIP"""
    id = models.CharField(max_length=20, primary_key=True)
    region = models.ForeignKey(Region, related_name='vpcs')
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.id)


class Instance(models.Model):
    # http://boto.readthedocs.org/en/latest/ref/ec2.html#boto.ec2.instance.InstanceState
    STATE_CHOICES = (
        (0, 'pending'),
        (16, 'running'),
        (32, 'shutting-down'),
        (48, 'terminated'),
        (64, 'stopping'),
        (80, 'stopped'),
    )
    id = models.CharField(max_length=20, primary_key=True)
    region = models.ForeignKey(Region, related_name='instances')
    name = models.CharField(max_length=255, blank=True, null=True)
    state = models.SmallIntegerField(choices=STATE_CHOICES,
        blank=True, null=True)
    launched = models.DateTimeField(blank=True, null=True)
    tags = JSONField(null=True, blank=True)
    security_groups = models.ManyToManyField('SecurityGroup', related_name='instances')
    vpc = models.ForeignKey(VPC, related_name='instances', blank=True, null=True)
    data = JSONField(blank=True, null=True)

    # bookkeeping
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.name:
            return '{} - {}'.format(self.id, self.name)
        return self.id

    @staticmethod
    def data_from_boto_ec2(boto_data, region=None):
        """
        Transform information from boto to something Instance can consume.
        """
        # WIP
        data = {k: v for k, v in boto_data.__dict__.items() if not k.startswith('_')}
        data.pop('block_device_mapping')
        data.pop('interfaces')
        data.pop('groups')
        data.pop('region')
        data.pop('connection')
        # region
        defaults = {
            'id': boto_data.id,
            'name': data['tags'].get('Name'),
            'state': boto_data.state_code,
            'launched': data['launch_time'],
            'data': data,
        }
        if boto_data.vpc_id:
            defaults['vpc'] = VPC.objects.get(pk=boto_data.vpc_id)
        if region is None:
            # TODO get region from data
            pass
        else:
            defaults['region'] = region
        return defaults


class SecurityGroup(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    # owner
    region = models.ForeignKey(Region, related_name='sgs')
    rules = models.ManyToManyField('SecurityGroupRule',
        related_name='sgs_inbound',
        help_text='Inbound')
    rules_egress = models.ManyToManyField('SecurityGroupRule',
        related_name='sgs_outbound',
        help_text='Outbound')
    tags = JSONField(null=True, blank=True)
    vpc = models.ForeignKey(VPC, related_name='sgs', blank=True, null=True)

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        name = self.tags['Name'] if 'Name' in self.tags else self.name
        return '{} ({})'.format(self.id, name)


class SecurityGroupRule(models.Model):
    """WIP

    Use a model instead of denormalized like tags for this use case: If there's
    a rule for an IP, changing the IP should affect all security groups that
    referenced that IP.
    """
    PROTOCOL_CHOICES = (
        ('tcp', 'tcp'),
        ('udp', 'udp'),
        ('icmp', 'icmp'),
    )
    protocol = models.CharField(max_length=4, choices=PROTOCOL_CHOICES)
    port_range = models.CommaSeparatedIntegerField(max_length=30,
        help_text='min, max')
    cidr = models.CharField(max_length=50, null=True, blank=True)
    source_group = models.ForeignKey(SecurityGroup, null=True, blank=True)
    # either cidr or source_group

    description = models.TextField(null=True, blank=True,
        help_text='User Description')

    class Meta:
        unique_together = ('protocol', 'port_range', 'cidr', 'source_group')

    def __unicode__(self):
        return '{} {} {}'.format(self.protocol, self.port_range, self.cidr or self.source_group)
