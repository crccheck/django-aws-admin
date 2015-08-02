# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aws_admin', '0005_auto_20150801_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityGroupRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('protocol', models.CharField(default='tcp', max_length=4, choices=[('tcp', 'tcp'), ('udp', 'udp'), ('icmp', 'icmp')])),
                ('port_range', models.CommaSeparatedIntegerField(help_text='min, max', max_length=30)),
                ('cidr', models.CharField(max_length=50)),
                ('description', models.TextField(help_text='User Description', null=True, blank=True)),
                ('source_group', models.ForeignKey(to='aws_admin.SecurityGroupRule')),
            ],
        ),
        migrations.RemoveField(
            model_name='securitygrouprules',
            name='source_group',
        ),
        migrations.AlterField(
            model_name='securitygroup',
            name='rules',
            field=models.ManyToManyField(help_text='Inbound', related_name='sgs_inbound', to='aws_admin.SecurityGroupRule'),
        ),
        migrations.AlterField(
            model_name='securitygroup',
            name='rules_egress',
            field=models.ManyToManyField(help_text='Outbound', related_name='sgs_outbound', to='aws_admin.SecurityGroupRule'),
        ),
        migrations.DeleteModel(
            name='SecurityGroupRules',
        ),
        migrations.AlterUniqueTogether(
            name='securitygrouprule',
            unique_together=set([('protocol', 'port_range', 'cidr', 'source_group')]),
        ),
    ]
