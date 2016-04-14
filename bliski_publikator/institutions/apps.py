from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class InstitutionsConfig(AppConfig):
    name = 'institutions'
    verbose_name = _("Institutions")
