from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import ugettext_lazy as _
from braces.views import (SelectRelatedMixin, LoginRequiredMixin, FormValidMessageMixin,
                          UserFormKwargsMixin)
from django.core.urlresolvers import reverse_lazy
from atom.views import DeleteMessageMixin
from .models import Monitoring
from .forms import MonitoringForm


class MonitoringListView(SelectRelatedMixin, ListView):
    model = Monitoring
    select_related = ['user']
    paginate_by = 25


class MonitoringDetailView(SelectRelatedMixin, DetailView):
    model = Monitoring
    select_related = ['user', ]


class MonitoringCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = Monitoring
    form_class = MonitoringForm

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class MonitoringUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserFormKwargsMixin,
                           FormValidMessageMixin, UpdateView):
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
