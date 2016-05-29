import factory
import factory.fuzzy
from . import models
from ..users.factories import UserFactory


class MonitoringFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'monitoring-%04d' % n)
    user = factory.SubFactory(UserFactory)
    description = factory.fuzzy.FuzzyText()
    instruction = factory.fuzzy.FuzzyText()
    active = True
    logo = factory.django.ImageField()
    max_point = 250

    class Meta:
        model = models.Monitoring
