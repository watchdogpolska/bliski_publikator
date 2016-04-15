# -*- coding: utf-8 -*-
from atom.ext.crispy_forms.forms import FormHorizontalMixin, SingleButtonMixin
from braces.forms import UserKwargModelFormMixin
from django import forms
from tinymce.widgets import TinyMCE

from .models import Page


class MonitoringMixin(object):
    def __init__(self, *args, **kwargs):
        monitoring = kwargs.pop('monitoring')
        super(MonitoringMixin, self).__init__(*args, **kwargs)
        self.instance.monitoring = monitoring


class PageForm(UserKwargModelFormMixin, MonitoringMixin, FormHorizontalMixin, SingleButtonMixin,
               forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Page
        fields = ['title', 'content', 'ordering']
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30})
        }


class MiniPageForm(UserKwargModelFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MiniPageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Page
        fields = ['title', 'ordering']

