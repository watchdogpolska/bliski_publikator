# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.MonitoringListView.as_view(),
        name="list"),
    url(r'^~create$', views.MonitoringCreateView.as_view(),
        name="create"),
    url(r'^monitorings-(?P<slug>[\w-]+)$', views.MonitoringDetailView.as_view(),
        name="details"),
    url(r'^monitorings-(?P<slug>[\w-]+)/~update$', views.MonitoringUpdateView.as_view(),
        name="update"),
    url(r'^monitorings-(?P<slug>[\w-]+)/~delete$', views.MonitoringDeleteView.as_view(),
        name="delete"),
]
