# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('state', models.SmallIntegerField(blank=True, null=True, choices=[(0, 'pending'), (16, 'running'), (32, 'shutting-down'), (48, 'terminated'), (64, 'stopping'), (80, 'stopped')])),
                ('launched', models.DateTimeField(null=True, blank=True)),
                ('tags', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('data', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.SlugField(unique=True, max_length=30)),
                ('name', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='SecurityGroup',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('tags', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('region', models.ForeignKey(related_name='sgs', to='aws_admin.Region')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SecurityGroupRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('protocol', models.CharField(max_length=4, choices=[('tcp', 'tcp'), ('udp', 'udp'), ('icmp', 'icmp')])),
                ('port_range', models.CommaSeparatedIntegerField(help_text='min, max', max_length=30)),
                ('cidr', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.TextField(help_text='User Description', null=True, blank=True)),
                ('source_group', models.ForeignKey(blank=True, to='aws_admin.SecurityGroup', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VPC',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('cidr', models.CharField(max_length=30, null=True, blank=True)),
                ('state', models.CharField(max_length=55, null=True, blank=True)),
                ('tags', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('region', models.ForeignKey(related_name='vpcs', to='aws_admin.Region')),
            ],
            options={
                'ordering': ('state',),
                'verbose_name': 'VPC',
            },
        ),
        migrations.AddField(
            model_name='securitygroup',
            name='rules',
            field=models.ManyToManyField(help_text='Inbound', related_name='sgs_inbound', to='aws_admin.SecurityGroupRule'),
        ),
        migrations.AddField(
            model_name='securitygroup',
            name='rules_egress',
            field=models.ManyToManyField(help_text='Outbound', related_name='sgs_outbound', to='aws_admin.SecurityGroupRule'),
        ),
        migrations.AddField(
            model_name='securitygroup',
            name='vpc',
            field=models.ForeignKey(related_name='sgs', blank=True, to='aws_admin.VPC', null=True),
        ),
        migrations.AddField(
            model_name='instance',
            name='region',
            field=models.ForeignKey(related_name='instances', to='aws_admin.Region'),
        ),
        migrations.AddField(
            model_name='instance',
            name='security_groups',
            field=models.ManyToManyField(related_name='instances', to='aws_admin.SecurityGroup'),
        ),
        migrations.AddField(
            model_name='instance',
            name='vpc',
            field=models.ForeignKey(related_name='instances', blank=True, to='aws_admin.VPC', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='securitygrouprule',
            unique_together=set([('protocol', 'port_range', 'cidr', 'source_group')]),
        ),
    ]
