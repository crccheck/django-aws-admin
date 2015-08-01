import logging

from django.conf import settings
from obj_update import obj_update_or_create
import boto.ec2

from .models import Region, Instance


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
        data = Instance.data_from_boto_ec2(boto_instance)
        instance_id = data.pop('id')
        instance, __ = obj_update_or_create(
            Instance,
            id=instance_id,
            defaults=data,
        )
        logger.debug(instance)
