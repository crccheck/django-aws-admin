# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aws_admin', '0003_instance'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='launched',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instance',
            name='state',
            field=models.SmallIntegerField(blank=True, null=True, choices=[(0, 'pending'), (16, 'running'), (32, 'shutting-down'), (48, 'terminated'), (64, 'stopping'), (80, 'stopped')]),
        ),
    ]
