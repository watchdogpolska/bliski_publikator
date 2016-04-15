from autoslug.fields import AutoSlugField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_bleach.models import BleachField
from model_utils.models import TimeStampedModel
from ..monitorings.models import Monitoring


class PageQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Page(TimeStampedModel):
    monitoring = models.ForeignKey(to=Monitoring, verbose_name=_("Monitoring"))
    title = models.CharField(verbose_name=_("Title"), max_length=50)
    slug = AutoSlugField(populate_from='title',
                         verbose_name=_("Slug"),
                         unique_with=['monitoring'])
    content = BleachField(blank=True)
    ordering = models.SmallIntegerField(verbose_name=_("Ordering"), default=0)
    objects = PageQuerySet.as_manager()

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        ordering = ['ordering', 'created', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('monitorings:pages:details', kwargs={'slug': self.slug,
                                                            'monitoring_slug': self.monitoring.slug}
                       )

    def get_update_url(self):
        return reverse('monitorings:pages:update', kwargs={'slug': self.slug,
                                                           'monitoring_slug': self.monitoring.slug}
                       )

    def get_delete_url(self):
        return reverse('monitorings:pages:delete', kwargs={'slug': self.slug,
                                                           'monitoring_slug': self.monitoring.slug}
                       )
