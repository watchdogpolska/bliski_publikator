# -*- coding: utf-8 -*-
from django import forms
from .models import Institution
from braces.forms import UserKwargModelFormMixin
from atom.ext.crispy_forms.forms import SingleButtonMixin


class InstitutionForm(UserKwargModelFormMixin, SingleButtonMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstitutionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Institution
        fields = ['name', 'regon', 'krs', 'region', 'monitorings']
