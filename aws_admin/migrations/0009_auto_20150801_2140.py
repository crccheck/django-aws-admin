# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aws_admin', '0008_auto_20150801_2020'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='securitygroup',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='instance',
            name='vpc',
            field=models.ForeignKey(related_name='instances', blank=True, to='aws_admin.VPC', null=True),
        ),
        migrations.AlterField(
            model_name='instance',
            name='security_groups',
            field=models.ManyToManyField(related_name='instances', to='aws_admin.SecurityGroup'),
        ),
    ]
