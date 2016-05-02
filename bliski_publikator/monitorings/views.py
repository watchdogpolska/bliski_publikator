import json
from atom.ext.crispy_forms.forms import BaseTableFormSet
from atom.views import DeleteMessageMixin
from braces.views import FormValidMessageMixin, SelectRelatedMixin, UserFormKwargsMixin
from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as _f

from django.views.generic import DeleteView, DetailView, ListView, TemplateView
from extra_views import InlineFormSet, NamedFormsetsMixin, UpdateWithInlinesView
from django.http import JsonResponse
from ..monitoring_pages.forms import MiniPageForm
from ..monitoring_pages.models import Page
from .forms import MonitoringForm
from .models import Monitoring
from django.utils.encoding import force_text
from ..questions.forms import QuestionForm, ConditionForm, ChoiceForm


NO_QUESTION = _f("Questions are required. No questions provided")

UNKNOWN_TARGET = _f("Attempt to create reference to non-exists target.")


class MonitoringListView(SelectRelatedMixin, ListView):
    model = Monitoring
    select_related = ['user']
    paginate_by = 25


class MonitoringDetailView(SelectRelatedMixin, DetailView):
    model = Monitoring
    select_related = ['user', ]


class MonitoringCreateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    model = Monitoring
    permission_required = 'monitorings.add_monitoring'
    template_name = 'monitorings/monitoring_form_angular.html'

    def error_list(self, form):
        return [(k, force_text(v[0])) for k, v in form.errors.items()]

    def error(self, **kwargs):
        kwargs['success'] = False
        return JsonResponse(kwargs, status=400)

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))

        # Validate
        # Validate monitoring
        form = MonitoringForm(data=data, user=self.request.user)
        if not form.is_valid():
            return self.error(errors=self.error_list(form))

        # Validate provided any questions
        questions = data.get('questions', None)
        if not questions:
            return self.error(error=NO_QUESTION)

        # Validate questions
        question_forms = [QuestionForm(data=x) for x in questions]
        if not all(x.is_valid() for x in question_forms):
            return self.error(errors=[self.error_list(x) for x in question_forms])

        # Validate condition by form
        condition_list = [condition
                          for question in questions if 'hideConditions' in question
                          for condition in question['hideConditions']]
        condition_forms = [ConditionForm(data=condition) for condition in condition_list]
        if not all(x.is_valid() for x in condition_forms):
            return self.error(errors=[self.error_list(x) for x in condition_forms])

        # Validate condition by target limit
        if not all(x.get('target', 0) < len(questions) and x.get('target', 0) >= 0
                   for x in condition_list):
            return self.error(error=UNKNOWN_TARGET)

        # Validate choices
        options_sets = [option for question in questions
                        if 'options' in question and question.get('type', None) == 'choice'
                        for option in question['options']]
        choices_forms = [ChoiceForm(data=options) for options in options_sets]
        if not all(x.is_valid() for x in choices_forms):
            return self.error(errors=[self.error_list(x) for x in choices_forms])

        # Save

        # Save monitoring
        monitoring = form.save()

        # Save question
        question_objs = []
        for i, x in enumerate(questions):
            related = {'monitoring': monitoring,
                       'created_by': self.request.user,
                       'order': i}
            question_objs.append(QuestionForm(data=x, related=related).save())

        # Save condition
        condition_objs = []
        for i, question in enumerate(questions):
            if not question.get('hideConditions', False):  # Skip if no conditions
                continue
            for condition in question['hideConditions']:
                related = {'related': question_objs[i],
                           'target': question_objs[condition.get('target', 0)]}
                condition_objs.append(ConditionForm(data=condition, related=related).save())

        # Save choices
        choice_objs = []
        for i, question in enumerate(questions):
            if 'options' not in question:  # Skip if no options
                continue
            if not question.get('type', None) != 'choice':  # Skip if bad type
                continue
            for j, option in enumerate(question['options']):
                related = {'question': question_objs[i], 'order': j}
                choice_objs.append(ChoiceForm(options, related=related).save())
        return JsonResponse({'success': True, 'url': monitoring.get_absolute_url()})


class PageInline(InlineFormSet):
    model = Page
    fields = ['title', 'ordering']
    form_class = MiniPageForm
    formset_class = BaseTableFormSet

    def get_factory_kwargs(self):  # Hack, see AndrewIngram/django-extra-views#121
        kwargs = super(PageInline, self).get_factory_kwargs()
        kwargs.pop('fields', None)
        return kwargs


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
    permission_required = 'monitorings.delete_monitoring'

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)


class MonitoringAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Monitoring.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
