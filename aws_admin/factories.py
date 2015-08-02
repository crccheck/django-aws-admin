import factory

from . import models


class VPCFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.VPC

    region_id = 1
    name = 'vpc'


class InstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Instance

    region_id = 1
