from dal import autocomplete
from django.views.generic import DetailView, ListView
from .models import JST


class JSTDetailView(DetailView):
    model = JST


class JSTListView(ListView):
    model = JST

    def get_queryset(self, *args, **kwargs):
        qs = super(JSTListView, self).get_queryset(*args, **kwargs)
        return qs.voivodeship()


class VoivodeshipAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = JST.objects.voivodeship().all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class CountyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = JST.objects.county().all()

        voivodeship = self.forwarded.get('voivodeship', None)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        if voivodeship:
            return qs.filter(parent=voivodeship)
        return qs.none()


class CommunityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = JST.objects.community().all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        county = self.forwarded.get('county', None)
        if county:
            return qs.filter(parent=county)
        return qs.none()
