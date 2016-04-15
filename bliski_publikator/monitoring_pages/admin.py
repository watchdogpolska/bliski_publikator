from django.contrib import admin

from .models import Page


class PageAdmin(admin.ModelAdmin):
    '''
        Admin View for Page
    '''
    list_display = ('title', 'monitoring')
    list_filter = ('monitoring',)
    search_fields = ('title', )

admin.site.register(Page, PageAdmin)
