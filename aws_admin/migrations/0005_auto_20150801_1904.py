# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('aws_admin', '0004_auto_20150801_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityGroup',
            fields=[
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('tags', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('region', models.ForeignKey(related_name='sgs', to='aws_admin.Region')),
            ],
        ),
        migrations.CreateModel(
            name='SecurityGroupRules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('protocol', models.CharField(default='tcp', max_length=4, choices=[('tcp', 'tcp'), ('udp', 'udp'), ('icmp', 'icmp')])),
                ('port_range', models.CommaSeparatedIntegerField(help_text='min, max', max_length=30)),
                ('cidr', models.CharField(max_length=50)),
                ('source_group', models.ForeignKey(to='aws_admin.SecurityGroupRules')),
            ],
        ),
        migrations.CreateModel(
            name='VPC',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('region', models.ForeignKey(related_name='vpcs', to='aws_admin.Region')),
            ],
        ),
        migrations.AddField(
            model_name='instance',
            name='tags',
            field=django_extensions.db.fields.json.JSONField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='securitygroup',
            name='rules',
            field=models.ManyToManyField(help_text='Inbound', related_name='sgs_inbound', to='aws_admin.SecurityGroupRules'),
        ),
        migrations.AddField(
            model_name='securitygroup',
            name='rules_egress',
            field=models.ManyToManyField(help_text='Outbound', related_name='sgs_outbound', to='aws_admin.SecurityGroupRules'),
        ),
        migrations.AddField(
            model_name='securitygroup',
            name='vpc',
            field=models.ForeignKey(related_name='sgs', blank=True, to='aws_admin.VPC', null=True),
        ),
        migrations.AddField(
            model_name='instance',
            name='security_groups',
            field=models.ManyToManyField(to='aws_admin.SecurityGroup'),
        ),
    ]
