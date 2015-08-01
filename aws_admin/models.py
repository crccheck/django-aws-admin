from __future__ import unicode_literals

from django.db import models
from django_extensions.db.fields.json import JSONField


class Region(models.Model):
    # ap-northeast-1
    # ap-southeast-1
    # ap-southeast-2
    # eu-central-1
    # eu-west-1
    # sa-east-1
    # us-east-1
    # us-west-1
    # us-west-2
    code = models.SlugField(max_length=30, unique=True)
    name = models.CharField(max_length=55)

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.code)


class Instance(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    region = models.ForeignKey(Region, related_name='instances')
    name = models.CharField(max_length=255, blank=True, null=True)
    # tags
    # security groups
    data = JSONField(blank=True, null=True)

    # bookkeeping
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.name:
            return '{} - {}'.format(self.id, self.name)
        return self.id
