from django.contrib import admin

from .models import Monitoring


class MonitoringAdmin(admin.ModelAdmin):
    '''
        Admin View for Monitoring
    '''
    list_display = ('name', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'description')

admin.site.register(Monitoring, MonitoringAdmin)
