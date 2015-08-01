from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models


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
