from atom.views import DeleteMessageMixin
from braces.views import (FormValidMessageMixin, SelectRelatedMixin,
                          UserFormKwargsMixin)
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from cached_property import cached_property
from .forms import PageForm
from .models import Page
from ..monitorings.models import Monitoring
from django.shortcuts import get_object_or_404


class MonitoringMixin(object):
    @cached_property
    def monitoring(self):
        return get_object_or_404(Monitoring, slug=self.kwargs['monitoring_slug'])

    def get_queryset(self, *args, **kwargs):
        qs = super(MonitoringMixin, self).get_queryset(*args, **kwargs)
        return qs.filter(monitoring=self.monitoring)

    def get_context_data(self, **kwargs):
        context = super(MonitoringMixin, self).get_context_data(**kwargs)
        context['monitoring'] = self.monitoring
        return context


class PageDetailView(SelectRelatedMixin, MonitoringMixin, DetailView):
    model = Page
    select_related = ['monitoring', ]


class PageCreateView(LoginRequiredMixin, PermissionRequiredMixin, MonitoringMixin,
                     UserFormKwargsMixin, CreateView):
    model = Page
    form_class = PageForm
    permission_required = 'monitoring_pages.add_page'

    def get_form_kwargs(self, *args, **kwargs):
        kw = super(PageCreateView, self).get_form_kwargs(*args, **kwargs)
        kw['monitoring'] = self.monitoring
        return kw

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class PageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MonitoringMixin,
                     UserFormKwargsMixin, FormValidMessageMixin, UpdateView):
    model = Page
    form_class = PageForm
    permission_required = 'monitoring_pages.change_page'

    def get_form_kwargs(self, *args, **kwargs):
        kw = super(PageUpdateView, self).get_form_kwargs(*args, **kwargs)
        kw['monitoring'] = self.monitoring
        return kw

    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)


class PageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MonitoringMixin,
                     DeleteMessageMixin, DeleteView):
    model = Page
    permission_required = 'monitoring_pages.delete_page'

    def get_success_url(self):
        return self.monitoring.get_absolute_url()

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)
