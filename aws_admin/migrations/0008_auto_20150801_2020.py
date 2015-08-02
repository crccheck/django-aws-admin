# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aws_admin', '0007_auto_20150801_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='securitygrouprule',
            name='source_group',
            field=models.ForeignKey(blank=True, to='aws_admin.SecurityGroup', null=True),
        ),
    ]
