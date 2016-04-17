from atom.ext.crispy_forms.forms import BaseTableFormSet
from atom.views import DeleteMessageMixin
from braces.views import FormValidMessageMixin, LoginRequiredMixin, SelectRelatedMixin, UserFormKwargsMixin
from dal import autocomplete
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from extra_views import CreateWithInlinesView, InlineFormSet, NamedFormsetsMixin, UpdateWithInlinesView

from ..monitoring_pages.models import Page
from .forms import MonitoringForm
from .models import Monitoring
from ..monitoring_pages.forms import MiniPageForm


class MonitoringListView(SelectRelatedMixin, ListView):
    model = Monitoring
    select_related = ['user']
    paginate_by = 25


class MonitoringDetailView(SelectRelatedMixin, DetailView):
    model = Monitoring
    select_related = ['user', ]


class PageInline(InlineFormSet):
    model = Page
    fields = ['title', 'ordering']
    form_class = MiniPageForm
    formset_class = BaseTableFormSet

    def get_factory_kwargs(self):
        kwargs = super(PageInline, self).get_factory_kwargs()
        kwargs.pop('fields', None)
        return kwargs


class MonitoringCreateView(LoginRequiredMixin, PermissionRequiredMixin, UserFormKwargsMixin,
                           NamedFormsetsMixin, CreateWithInlinesView):
    inlines = [PageInline, ]
    inlines_names = ['pages']
    model = Monitoring
    form_class = MonitoringForm
    permission_required = 'monitorings.add_monitoring'

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class MonitoringUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserFormKwargsMixin,
                           FormValidMessageMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    inlines = [PageInline, ]
    inlines_names = ['pages', ]
    model = Monitoring
    form_class = MonitoringForm
    permission_required = 'monitorings.change_monitoring'

    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)


class MonitoringDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteMessageMixin,
                           DeleteView):
    model = Monitoring
    success_url = reverse_lazy('monitorings:list')
    permission_required = 'monitorings.change_monitoring'

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)


class MonitoringAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Monitoring.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
