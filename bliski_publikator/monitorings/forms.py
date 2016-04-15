# -*- coding: utf-8 -*-
from atom.ext.crispy_forms.forms import FormHorizontalMixin, SingleButtonMixin
from braces.forms import UserKwargModelFormMixin
from dal import autocomplete
from django import forms
from tinymce.widgets import TinyMCE

from .models import Monitoring


class MonitoringForm(UserKwargModelFormMixin, FormHorizontalMixin, SingleButtonMixin,
                     forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MonitoringForm, self).__init__(*args, **kwargs)
        if not self.instance.user_id:
            self.instance.user = self.user

    class Meta:
        model = Monitoring
        fields = ['name', 'description', 'institutions', 'active']
        widgets = {
            'institutions': autocomplete.ModelSelect2Multiple(url='institutions:autocomplete'),
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30})
        }
