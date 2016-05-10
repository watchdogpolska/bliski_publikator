# -*- coding: utf-8 -*-
from atom.ext.crispy_forms.forms import FormHorizontalMixin, SingleButtonMixin
from braces.forms import UserKwargModelFormMixin
from dal import autocomplete
from django import forms
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext_lazy as _

from ..institutions.models import Institution
from .models import Monitoring
from .utils import M2MFieldFormMixin


class MonitoringForm(UserKwargModelFormMixin, FormHorizontalMixin, SingleButtonMixin,
                     M2MFieldFormMixin, forms.ModelForm):
    institutions = forms.ModelMultipleChoiceField(queryset=Institution.objects.all(),
                                                  label=_("Institutions"),
                                                  required=False,
                                                  widget=autocomplete.ModelSelect2Multiple(url='institutions:autocomplete'))

    def __init__(self, *args, **kwargs):
        super(MonitoringForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['institutions'].initial = self.instance.institutions.all()

        if not self.instance.user_id:
            self.instance.user = self.user

    def save(self, *args, **kwargs):
        super(MonitoringForm, self).save(*args, **kwargs)
        self.save_m2m_field(field='institutions',
                            left='monitoring',
                            right='institution')
        return self.instance

    class Meta:
        model = Monitoring
        fields = ['name', 'description', 'active', 'max_point', ]
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
