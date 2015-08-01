from django.test import TestCase
import boto.ec2
import mock

from ..factories import InstanceFactory
from ..models import Instance


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
            tags={'Name': 'foobar'},
            state_code=16,  # running
        )
        data = Instance.data_from_boto_ec2(boto_data)
        instance_id = data.pop('id')
        instance = InstanceFactory(id=instance_id, **data)
        print instance
        self.assertEqual(instance.id, boto_data.id)
        self.assertEqual(instance.state, boto_data.state_code)
