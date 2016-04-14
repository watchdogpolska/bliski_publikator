# -*- coding: utf-8 -*-
from django import forms
from .models import Monitoring
from braces.forms import UserKwargModelFormMixin
from atom.ext.crispy_forms.forms import SingleButtonMixin


class MonitoringForm(UserKwargModelFormMixin, SingleButtonMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MonitoringForm, self).__init__(*args, **kwargs)
        if not self.instance.user_id:
            self.instance.user = self.user

    class Meta:
        model = Monitoring
        fields = ['name', 'description', 'institutions', 'active']
