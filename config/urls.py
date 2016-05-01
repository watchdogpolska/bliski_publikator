# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from rest_framework import routers
from bliski_publikator.institutions.viewsets import InstitutionViewSet
from bliski_publikator.users.viewsets import UserViewSet
from bliski_publikator.teryt.viewsets import (JSTViewSet, JednostkaAdministracyjnaViewSet,
                                              CategoryViewSet)
from bliski_publikator.monitorings.viewsets import MonitoringViewSet
from bliski_publikator.monitoring_pages.viewsets import PageViewSet

router = routers.DefaultRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'users', UserViewSet)
router.register(r'teryt', JSTViewSet)
router.register(r'teryt', JednostkaAdministracyjnaViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'monitorings', MonitoringViewSet)
router.register(r'monitoring_pages', PageViewSet)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name="about"),

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
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception("Permission Denied")}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
    ]
