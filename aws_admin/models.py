from __future__ import unicode_literals

from django.db import models
from django_extensions.db.fields.json import JSONField


class Region(models.Model):
    code = models.SlugField(max_length=30, unique=True)
    name = models.CharField(max_length=55)

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.code)


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
    # tags
    # security groups
    data = JSONField(blank=True, null=True)

    # bookkeeping
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.name:
            return '{} - {}'.format(self.id, self.name)
        return self.id
