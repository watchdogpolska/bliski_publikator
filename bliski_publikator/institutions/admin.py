from django.contrib import admin

# Register your models here.
from .models import Institution


class InstitutionAdmin(admin.ModelAdmin):
    '''
        Admin View for Instutition
    '''
    list_display = ('name', 'email', 'regon', 'krs')
    list_filter = ('user', )
    search_fields = ('name', 'email', 'regon', 'krs')

admin.site.register(Institution, InstitutionAdmin)
