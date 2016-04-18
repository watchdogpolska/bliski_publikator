import factory
import factory.fuzzy
from . import models
from ..users.factories import UserFactory
from ..teryt.factories import JSTFactory


class InstitutionFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Institution-%04d' % n)
    user = factory.SubFactory(UserFactory)
    email = factory.LazyAttribute(lambda x: x.name+"@example.com")
    region = factory.SubFactory(JSTFactory)

    class Meta:
        model = models.Institution
