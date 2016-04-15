import factory
import factory.fuzzy
from . import models
from ..monitorings.factories import MonitoringFactory


class PageFactory(factory.django.DjangoModelFactory):
    monitoring = factory.SubFactory(MonitoringFactory)
    title = factory.Sequence(lambda n: 'page-monitoring-%04d' % n)
    content = factory.fuzzy.FuzzyText()
    ordering = 1

    class Meta:
        model = models.Page
