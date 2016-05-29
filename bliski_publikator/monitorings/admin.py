from django import forms
from django.contrib import admin

from .models import Monitoring
from tinymce.widgets import TinyMCE


class MonitoringForm(forms.ModelForm):

    class Meta:
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'instruction': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


class MonitoringAdmin(admin.ModelAdmin):
    '''
        Admin View for Monitoring
    '''
    form = MonitoringForm
    list_display = ('name', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'description')

admin.site.register(Monitoring, MonitoringAdmin)
