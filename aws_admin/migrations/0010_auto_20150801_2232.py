# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('aws_admin', '0009_auto_20150801_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='vpc',
            name='cidr',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='vpc',
            name='state',
            field=models.CharField(max_length=55, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='vpc',
            name='tags',
            field=django_extensions.db.fields.json.JSONField(null=True, blank=True),
        ),
    ]
