# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<monitoring_slug>[\w-]+)/~create$', views.PageCreateView.as_view(),
        name="create"),
    url(r'^(?P<monitoring_slug>[\w-]+)/(?P<slug>[\w-]+)$', views.PageDetailView.as_view(),
        name="details"),
    url(r'^(?P<monitoring_slug>[\w-]+)/(?P<slug>[\w-]+)/~update$', views.PageUpdateView.as_view(),
        name="update"),
    url(r'^(?P<monitoring_slug>[\w-]+)/(?P<slug>[\w-]+)/~delete$', views.PageDeleteView.as_view(),
        name="delete"),
]
