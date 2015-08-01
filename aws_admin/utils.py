import logging

from django.conf import settings
from obj_update import obj_update_or_create
import boto.ec2

from aws_admin.models import Region, Instance


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
        data = {k: v for k, v in boto_instance.__dict__.items() if not k.startswith('_')}
        data.pop('block_device_mapping')
        data.pop('interfaces')
        data.pop('groups')
        data.pop('region')
        data.pop('connection')
        defaults = {
            'name': boto_instance.tags.get('Name'),
            'region': region,
            'data': data,
        }
        instance, __ = obj_update_or_create(
            Instance,
            id=boto_instance.id,
            defaults=defaults,
        )
        logger.debug(instance)


# DELETEME
if __name__ == '__main__':
    pull_ec2()
