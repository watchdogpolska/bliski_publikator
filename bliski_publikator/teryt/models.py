from teryt_tree.models import JednostkaAdministracyjna
from django.core.urlresolvers import reverse
from cached_property import cached_property

class JST(JednostkaAdministracyjna):

    @cached_property
    def institution_area(self):
        return self.institution_set.model.objects.area(self).all()

    def get_absolute_url(self):
        return reverse('teryt:details', kwargs={'slug': self.slug})

    class Meta:
        proxy = True
