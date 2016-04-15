from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class MonitoringsConfig(AppConfig):
    name = 'monitoring_pages'
    verbose_name = _("Monitorings pages")
