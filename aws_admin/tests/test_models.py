from django.test import TestCase
import boto.ec2
import mock

from ..factories import InstanceFactory
from ..models import Instance
from ..utils import data_from_boto_ec2


class InstanceTests(TestCase):
    def test_creation_from_boto(self):
        boto_data = mock.MagicMock(
            spec=boto.ec2.instance,
            id='i-1337',
            block_device_mapping='TODO',
            interfaces='TODO',
            groups='TODO',
            region='NOOP',
            connection='TODO',
        )
        # kind of more of a test of utils
        data = data_from_boto_ec2(boto_data)
        instance = InstanceFactory(id='i-1337', data=data)
        print instance
