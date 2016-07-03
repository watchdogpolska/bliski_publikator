# -*- coding: utf-8 -*-
from dal import autocomplete
from django.utils.translation import ugettext as _
from django_filters import FilterSet
from django_filters.filters import ModelChoiceFilter
from teryt_tree.dal_ext.filters import CommunityFilter, CountyFilter, VoivodeshipFilter

from ..monitorings.models import Monitoring
from .models import Institution


class InstitutionFilter(FilterSet):
    voivodeship = VoivodeshipFilter(
        widget=autocomplete.ModelSelect2(url='teryt:voivodeship-autocomplete')
    )
    county = CountyFilter(
        widget=autocomplete.ModelSelect2(url='teryt:county-autocomplete',
                                         forward=['voivodeship'])
    )
    community = CommunityFilter(
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
