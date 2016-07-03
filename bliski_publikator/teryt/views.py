from __future__ import unicode_literals
from django.views.generic import DetailView, ListView
from .models import JST


class JSTDetailView(DetailView):
    model = JST


class JSTListView(ListView):
    model = JST

    def get_queryset(self, *args, **kwargs):
        qs = super(JSTListView, self).get_queryset(*args, **kwargs)
        return qs.voivodeship()
