import logging

from django.conf import settings
from obj_update import obj_update_or_create
import boto.ec2

from .models import Region, Instance, SecurityGroup, SecurityGroupRule, VPC


logger = logging.getLogger(__name__)


def pull_ec2(region=None):
    if region is None:
        region = Region.objects.get(id=1)  # as defined by our initial data
    conn = boto.ec2.connect_to_region(
        region.code,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    instances = conn.get_only_instances()
    for boto_instance in instances:
        data = Instance.data_from_boto_ec2(boto_instance, region=region)
        instance_id = data.pop('id')
        instance, __ = obj_update_or_create(
            Instance,
            id=instance_id,
            defaults=data,
        )
        # TODO don't do unnecessary SQL
        instance.security_groups.clear()
        for group in boto_instance.groups:
            security_group, __ = SecurityGroup.objects.get_or_create(
                id=group.id, region=region)
            instance.security_groups.add(security_group)
        logger.debug(instance)


def pull_security_groups(region=None):
    if region is None:
        region = Region.objects.get(id=1)  # as defined by our initial data
    conn = boto.ec2.connect_to_region(
        region.code,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    sg_cache = {}
    rs = conn.get_all_security_groups()
    for group in rs:
        vpc, __ = VPC.objects.get_or_create(id=group.vpc_id, defaults={'region': region})
        defaults = {
            'description': group.description,
            'name': group.name,
            'region': region,
            'tags': group.tags,
            'vpc': vpc,
        }
        security_group, __ = obj_update_or_create(
            SecurityGroup,
            id=group.id,
            defaults=defaults,
        )
        sg_cache[group.id] = security_group
    # Do a second pass in case we run into a rule that grants a security group
    # we don't know about yet
    for group in rs:
        security_group = sg_cache[group.id]
        # TODO don't do unnecessary SQL
        security_group.rules.clear()
        for rule in group.rules:
            print rule.from_port, rule.to_port
            defaults = dict(
                protocol=rule.ip_protocol,
                port_range=[int(rule.from_port or 0), int(rule.to_port or 0)],
            )
            for grant in rule.grants:
                if grant.group_id:
                    defaults['source_group'] = sg_cache[grant.group_id]
                    defaults['cidr'] = None
                else:
                    defaults['source_group'] = None
                    defaults['cidr'] = grant.cidr_ip

                print defaults
                sg_rule, __ = SecurityGroupRule.objects.get_or_create(**defaults)
                security_group.rules.add(sg_rule)

        # TODO don't do unnecessary SQL
        security_group.rules_egress.clear()
        for rule in group.rules:
            defaults = dict(
                protocol=rule.ip_protocol,
                port_range=[int(rule.from_port or 0), int(rule.to_port or 0)],
            )
            for grant in rule.grants:
                if grant.group_id:
                    defaults['source_group'] = sg_cache[grant.group_id]
                    defaults['cidr'] = None
                else:
                    defaults['source_group'] = None
                    defaults['cidr'] = grant.cidr_ip

                sg_rule, __ = SecurityGroupRule.objects.get_or_create(**defaults)
                security_group.rules_egress.add(sg_rule)
