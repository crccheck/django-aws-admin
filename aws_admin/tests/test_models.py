from __future__ import unicode_literals

from django.test import TestCase
import boto.ec2
import mock

from ..factories import VPCFactory, InstanceFactory
from ..models import Instance


class InstanceTests(TestCase):
    def test_creation_from_boto(self):
        # setup
        VPCFactory(id='vpc-123')

        boto_data = mock.MagicMock(
            spec=boto.ec2.instance,
            id='i-1337',
            tags={'Name': 'foobar'},
            state_code=16,  # running
            launch_time='2015-08-01T18:41:23.000Z',
            vpc_id='vpc-123',
            block_device_mapping='TODO',
            interfaces='TODO',
            groups='TODO',
            region='NOOP',
            connection='TODO',
        )
        data = Instance.data_from_boto_ec2(boto_data)
        instance_id = data.pop('id')
        instance = InstanceFactory(id=instance_id, **data)
        # refresh model cache
        instance = Instance.objects.get(id=instance.id)
        self.assertEqual(instance.id, boto_data.id)
        self.assertEqual(instance.name, 'foobar')
        self.assertEqual(instance.state, boto_data.state_code)
        self.assertEqual(instance.launched.isoformat(), '2015-08-01T18:41:23+00:00')
