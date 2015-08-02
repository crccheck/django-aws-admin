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
    security_groups = models.ManyToManyField('SecurityGroup')
    data = JSONField(blank=True, null=True)

    # bookkeeping
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.name:
            return '{} - {}'.format(self.id, self.name)
        return self.id

    @staticmethod
    def data_from_boto_ec2(boto_instance, region=None):
        """
        Transform information from boto to something Instance can consume.
        """
        # WIP
        data = {k: v for k, v in boto_instance.__dict__.items() if not k.startswith('_')}
        data.pop('block_device_mapping')
        data.pop('interfaces')
        data.pop('groups')
        data.pop('region')
        data.pop('connection')
        # region
        defaults = {
            'id': boto_instance.id,
            'name': data['tags'].get('Name'),
            'state': boto_instance.state_code,
            'launched': data['launch_time'],
            'data': data,
        }
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
    rules = models.ManyToManyField('SecurityGroupRules',
        related_name='sgs_inbound',
        help_text='Inbound')
    rules_egress = models.ManyToManyField('SecurityGroupRules',
        related_name='sgs_outbound',
        help_text='Outbound')
    tags = JSONField(null=True, blank=True)
    vpc = models.ForeignKey(VPC, related_name='sgs', blank=True, null=True)

    def __unicode__(self):
        if 'Name' in self.tags:
            return self.tags['Name']
        return self.name


class SecurityGroupRules(models.Model):
    """WIP"""
    PROTOCOL_CHOICES = (
        ('tcp', 'tcp'),
        ('udp', 'udp'),
        ('icmp', 'icmp'),
    )
    protocol = models.CharField(max_length=4, choices=PROTOCOL_CHOICES, default='tcp')
    port_range = models.CommaSeparatedIntegerField(max_length=30,
        help_text='min, max')
    cidr = models.CharField(max_length=50)
    source_group = models.ForeignKey('self')
    # either cidr or source_group
