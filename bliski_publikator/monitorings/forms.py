# -*- coding: utf-8 -*-
from atom.ext.crispy_forms.forms import FormHorizontalMixin, SingleButtonMixin
from braces.forms import UserKwargModelFormMixin
from dal import autocomplete
from django import forms
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext_lazy as _


from .models import Monitoring, MonitoringInstitution
from ..institutions.models import Institution


class MonitoringForm(UserKwargModelFormMixin, FormHorizontalMixin, SingleButtonMixin,
                     forms.ModelForm):
    institutions = forms.ModelMultipleChoiceField(queryset=Institution.objects.all(),
                                                  label=_("institutions"),
                                                  required=False)

    def __init__(self, *args, **kwargs):
        super(MonitoringForm, self).__init__(*args, **kwargs)
        if not self.instance.user_id:
            self.instance.user = self.user

    def save(self, *args, **kwargs):
        super(MonitoringForm, self).save(*args, **kwargs)
        MonitoringInstitution.objects.bulk_create(
            [MonitoringInstitution(monitoring=self.instance, institution=institution)
             for institution in self.cleaned_data['institutions']])
        return self.instance

    class Meta:
        model = Monitoring
        fields = ['name', 'description', 'active', 'max_point']
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'institutions': autocomplete.ModelSelect2Multiple(url='institutions:autocomplete'),
        }
