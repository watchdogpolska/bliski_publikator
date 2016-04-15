from autoslug.fields import AutoSlugField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from ..teryt.models import JST


class InstitutionQuerySet(models.QuerySet):
    def area(self, jst):
        return self.filter(region__tree_id=jst.tree_id,
                           region__lft__range=(jst.lft, jst.rght))


@python_2_unicode_compatible
class Institution(TimeStampedModel):
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    slug = AutoSlugField(populate_from='name', verbose_name=_("Slug"), unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    email = models.EmailField(verbose_name=_("E-mail"), blank=True)
    region = models.ForeignKey(JST,
                               limit_choices_to={'category__level': 3},
                               verbose_name=_('Unit of administrative division'),
                               db_index=True)
    regon = models.CharField(verbose_name=_("REGON"), max_length=14, blank=True)  # TODO: RegonField
    krs = models.CharField(verbose_name=_("KRS"), max_length=11, blank=True)  # TODO: KRSField
    monitorings = models.ManyToManyField(to='monitorings.Monitoring',
                                         through='monitorings.monitoring_institutions')
    objects = InstitutionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Institution")
        verbose_name_plural = _("Institutions")
        ordering = ['created', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('institutions:details', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('institutions:update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('institutions:delete', kwargs={'slug': self.slug})

    @staticmethod
    def get_add_url():
        return reverse('institutions:create')
