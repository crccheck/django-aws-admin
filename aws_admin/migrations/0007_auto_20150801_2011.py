# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aws_admin', '0006_auto_20150801_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='securitygrouprule',
            name='cidr',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='securitygrouprule',
            name='protocol',
            field=models.CharField(max_length=4, choices=[('tcp', 'tcp'), ('udp', 'udp'), ('icmp', 'icmp')]),
        ),
        migrations.AlterField(
            model_name='securitygrouprule',
            name='source_group',
            field=models.ForeignKey(blank=True, to='aws_admin.SecurityGroupRule', null=True),
        ),
    ]
