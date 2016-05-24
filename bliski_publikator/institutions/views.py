from atom.views import DeleteMessageMixin
from braces.views import FormValidMessageMixin, SelectRelatedMixin, UserFormKwargsMixin
from cached_property import cached_property
from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from ..monitorings.models import Monitoring
from .filters import InstitutionFilter
from .forms import InstitutionForm
from .models import Institution


class InstitutionListView(SelectRelatedMixin, FilterView):
    filterset_class = InstitutionFilter
    model = Institution
    select_related = ['region', ]
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        qs = super(InstitutionListView, self).get_queryset(*args, **kwargs)
        return qs.with_stats()


class InstitutionDetailView(SelectRelatedMixin, DetailView):
    model = Institution
    select_related = ['region', ]

    def get_queryset(self, *args, **kwargs):
        qs = super(InstitutionDetailView, self).get_queryset(*args, **kwargs)
        return qs.with_stats()


class InstitutionCreateView(LoginRequiredMixin, PermissionRequiredMixin, UserFormKwargsMixin,
                            CreateView):
    model = Institution
    form_class = InstitutionForm
    permission_required = 'institutions.add_institution'

    @cached_property
    def monitoring(self):
        if 'monitoring_slug' in self.kwargs:
            return get_object_or_404(Monitoring, slug=self.kwargs['monitoring_slug'])
        return None

    def get_initial(self):
        return {'monitorings': [self.monitoring]}

    def get_context_data(self, *args, **kwargs):
        context = super(InstitutionCreateView, self).get_context_data(*args, **kwargs)
        if self.monitoring:
            context['monitoring'] = self.monitoring
        return context

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class InstitutionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserFormKwargsMixin,
                            FormValidMessageMixin, UpdateView):
    model = Institution
    form_class = InstitutionForm
    permission_required = 'institutions.change_institution'

    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)


class InstitutionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteMessageMixin,
                            DeleteView):
    model = Institution
    success_url = reverse_lazy('monitorings:list')
    permission_required = 'institutions.delete_institution'

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)


class InstitutionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Institution.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
