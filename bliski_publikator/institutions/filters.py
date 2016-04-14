# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django_filters import FilterSet

from .models import Institution


class InstitutionFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super(InstitutionFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Institution
        fields = ['region', 'monitoring']
