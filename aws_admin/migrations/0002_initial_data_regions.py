# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


REGIONS = (
    ('us-east-1', 'US East (N. Virginia)'),
    ('us-west-1', 'US West (N. California)'),
    ('us-west-2', 'US West (Oregon)'),
    ('ap-northeast-1', 'Asia Pacific (Tokyo)'),
    ('ap-southeast-1', 'Asia Pacific (Singapore)'),
    ('ap-southeast-2', 'Asia Pacific (Sydney)'),
    ('eu-central-1', 'EU (Frankfurt)'),
    ('eu-west-1', 'EU (Ireland)'),
    ('sa-east-1', 'South America (Sao Paulo)'),
)


def initial_data(apps, schema_editor):
    Region = apps.get_model('aws_admin', 'Region')
    for code, name in REGIONS:
        Region.objects.get_or_create(code=code, name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('aws_admin', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_data),
    ]
