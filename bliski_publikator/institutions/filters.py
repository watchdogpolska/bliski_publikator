# -*- coding: utf-8 -*-
from django_filters import FilterSet
from django_filters.filters import ModelChoiceFilter
from dal import autocomplete
from ..teryt.models import JST
from django.utils.translation import ugettext as _

from .models import Institution
from ..monitorings.models import Monitoring


class InstitutionFilter(FilterSet):
    voivodeship = ModelChoiceFilter(
        label=_("Voivodeship"),
        required=False,
        queryset=JST.objects.voivodeship().all(),
        action=lambda q, v: q.area(v),
        widget=autocomplete.ModelSelect2(url='teryt:voivodeship-autocomplete')
    )
    county = ModelChoiceFilter(
        label=_("County"),
        required=False,
        queryset=JST.objects.county().all(),
        action=lambda q, v: q.area(v),
        widget=autocomplete.ModelSelect2(url='teryt:county-autocomplete',
                                         forward=['voivodeship'])
    )
    community = ModelChoiceFilter(
        label=_("Community"),
        required=False,
        queryset=JST.objects.community().all(),
        action=lambda q, v: q.area(v),
        widget=autocomplete.ModelSelect2(url='teryt:community-autocomplete',
                                         forward=['county'])
    )
    monitoring = ModelChoiceFilter(
        label=_("Monitoring"),
        required=False,
        queryset=Monitoring.objects.all(),
        widget=autocomplete.ModelSelect2(url='monitorings:autocomplete'),
    )

    def __init__(self, *args, **kwargs):
        self.monitoring = kwargs.pop('monitoring', None)
        super(InstitutionFilter, self).__init__(*args, **kwargs)
        if self.monitoring:
            qs = Monitoring.objects.exclude(pk=self.monitoring.pk).all()
            self.filters['monitoring'].field.queryset = qs

    class Meta:
        model = Institution
        fields = ['monitoring']
