from teryt_tree.models import JednostkaAdministracyjna
from django.core.urlresolvers import reverse


class JST(JednostkaAdministracyjna):
    def get_absolute_url(self):
        return reverse('teryt:details', kwargs={'slug': self.slug})

    class Meta:
        proxy = True
