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
    url(r'^~create$', views.MonitoringAPICreateView.as_view(),
        name="create"),
    url(r'^(?P<slug>[\w-]+)$', views.MonitoringDetailView.as_view(),
        name="details"),
    url(r'^(?P<slug>[\w-]+)/~update$', views.MonitoringUpdateView.as_view(),
        name="update"),
    url(r'^(?P<slug>[\w-]+)/~reinitalize$', views.MonitoringAPIUpdateView.as_view(),
        name="reinitalize"),
    url(r'^(?P<slug>[\w-]+)/~delete$', views.MonitoringDeleteView.as_view(),
        name="delete"),
    # Extra action
    url(r'^(?P<slug>[\w-]+)/~assign$', views.MonitoringAssignUpdateView.as_view(),
        name="assign"),

    # Answer views
    url(r'^(?P<pk>[\d]+)/api$', views.MonitoringApiDetailView.as_view(), name="details_api"),
    url(r'^(?P<slug>[\w-]+)/(?P<institution_slug>[\w-]+)/~assign$',
        views.MonitoringSignleAssingUpdateView.as_view(),
        name="assign"),
    url(r'^(?P<slug>[\w-]+)/(?P<institution_slug>[\w-]+)/~sheets$',
        views.MonitoringInstitutionDetailView.as_view(),
        name="sheet_list"),
    url(r'^(?P<slug>[\w-]+)/(?P<institution_slug>[\w-]+)/~answers$',
        views.SheetCreateView.as_view(),
        name="sheet_create"),
    url(r'^(?P<slug>[\w-]+)/institution-(?P<institution_slug>[\w-]+)$',
        views.MonitoringDetailView.as_view(),
        name="institution_detail"),
    url(r'^', include("bliski_publikator.monitoring_pages.urls", namespace="pages")),
]
