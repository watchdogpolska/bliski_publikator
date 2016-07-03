# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bliski_publikator.institutions.viewsets import InstitutionViewSet
from bliski_publikator.monitoring_pages.viewsets import PageViewSet
from bliski_publikator.monitorings.viewsets import MonitoringViewSet
from bliski_publikator.questions.viewsets import (
    QuestionViewSet,
    SheetViewSet
)

from teryt_tree.rest_framework_ext.viewsets import JednostkaAdministracyjnaViewSet
from bliski_publikator.users.viewsets import UserViewSet

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'users', UserViewSet)
router.register(r'teryt', JednostkaAdministracyjnaViewSet)
router.register(r'monitorings', MonitoringViewSet)
router.register(r'monitoring_pages', PageViewSet)

router.register(r'questions', QuestionViewSet)
router.register(r'sheet', SheetViewSet)


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r'^contact/$', TemplateView.as_view(template_name='pages/contact.html'), name="contact"),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include("bliski_publikator.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^monitorings/', include("bliski_publikator.monitorings.urls", namespace="monitorings")),
    url(r'^institutions/', include("bliski_publikator.institutions.urls",
                                   namespace="institutions")),
    url(r'^teryt/', include("bliski_publikator.teryt.urls", namespace="teryt")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^angular2/$', TemplateView.as_view(template_name='pages/angular2-example.html'),
            name="ng2-example"),
        url(r'^api/monitoring/[0-9]+$', TemplateView.as_view(
            template_name='api/monitoring-1-get-ok.json'), name="monitoring-1-get-ok"),
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception("Permission Denied")}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
    ]
