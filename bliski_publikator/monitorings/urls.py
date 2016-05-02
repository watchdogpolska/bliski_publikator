# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.MonitoringListView.as_view(),
        name="list"),
    url(r'^~autocomplete$', views.MonitoringAutocomplete.as_view(),
        name="autocomplete"),

    # CRUD
    url(r'^~create$', views.MonitoringCreateView.as_view(),
        name="create"),
    url(r'^(?P<slug>[\w-]+)$', views.MonitoringDetailView.as_view(),
        name="details"),
    url(r'^(?P<slug>[\w-]+)/~update$', views.MonitoringUpdateView.as_view(),
        name="update"),
    url(r'^(?P<slug>[\w-]+)/~delete$', views.MonitoringDeleteView.as_view(),
        name="delete"),
    # Extra action
    url(r'^(?P<slug>[\w-]+)/~assign$', views.MonitoringAssignUpdateView.as_view(),
        name="assign"),

    # Answer views
    url(r'^(?P<slug>[\w-]+)/(?P<institution_slug>[\w-]+)/~answer$',
        views.MonitoringAnswerView.as_view(),
        name="institution_answer"),
    url(r'^(?P<slug>[\w-]+)/(?P<institution_slug>[\w-]+)$',
        views.MonitoringDetailView.as_view(),
        name="institution_detail"),

    url(r'^', include("bliski_publikator.monitoring_pages.urls", namespace="pages")),
]
