# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('aws_admin', '0002_initial_data_regions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('data', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('region', models.ForeignKey(related_name='instances', to='aws_admin.Region')),
            ],
        ),
    ]
