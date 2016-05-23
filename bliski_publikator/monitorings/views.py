import json

from atom.ext.crispy_forms.forms import BaseTableFormSet
from atom.views import DeleteMessageMixin
from braces.views import (
    FormValidMessageMixin,
    JSONResponseMixin,
    PrefetchRelatedMixin,
    SelectRelatedMixin,
    UserFormKwargsMixin
)
from cached_property import cached_property
from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _f
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DeleteView, DetailView, ListView, TemplateView
from django_filters.views import FilterView
from extra_views import InlineFormSet, NamedFormsetsMixin, UpdateWithInlinesView

from ..institutions.filters import InstitutionFilter
from ..institutions.models import Institution
from ..monitoring_pages.forms import MiniPageForm
from ..monitoring_pages.models import Page
from ..questions.forms import ChoiceForm, ConditionForm, QuestionForm, get_form_cls_for_question
from ..questions.models import Question, Sheet
from .forms import MonitoringForm
from .models import Monitoring, MonitoringInstitution

NO_QUESTION = _f("Questions are required. No questions provided")

UNKNOWN_TARGET = _f("Attempt to create reference to non-exists target.")


class CustomJSONResponseMixin(object):
    def error_list(self, form):
        return [(k, force_text(v[0])) for k, v in form.errors.items()]

    def error(self, **kwargs):
        kwargs['success'] = False
        # transaction.rollback() # TODO: Rollback on error
        return JsonResponse(kwargs, status=400)


class MonitoringListView(SelectRelatedMixin, ListView):
    model = Monitoring
    select_related = ['user']
    paginate_by = 25


class MonitoringDetailView(SelectRelatedMixin, DetailView):
    model = Monitoring
    select_related = ['user', ]

    def get_monitoringinstitution_qs(self):
        return MonitoringInstitution.objects.\
            filter(monitoring=self.object).\
            with_point().\
            select_related('institution').\
            all()

    def get_context_data(self, **kwargs):
        context = super(MonitoringDetailView, self).get_context_data(**kwargs)
        context['monitoringinstitution'] = self.get_monitoringinstitution_qs()
        return context


class MonitoringCreateView(LoginRequiredMixin, CustomJSONResponseMixin, PermissionRequiredMixin,
                           TemplateView):
    model = Monitoring
    permission_required = 'monitorings.add_monitoring'
    template_name = 'monitorings/monitoring_form_monitoring.html'

    def post(self, *args, **kwargs):  # TODO: Transactions in MonitoringCreateView
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
        def field_mapping(x):
            x['count'] = json.dumps(x.get('countConditions', []))
            return x
        question_forms = [QuestionForm(data=field_mapping(x)) for x in questions]
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
                           'target': question_objs[condition.get('target', 0)],
                           'value': condition.get('value', '') or ''}
                condition_objs.append(ConditionForm(data=condition, related=related).save())

        # Save choices
        choice_objs = []
        for i, question in enumerate(questions):
            if 'options' not in question:  # Skip if no options
                continue
            if question.get('type', None) != 'choice':  # Skip if bad type
                continue
            for j, option in enumerate(question['options']):
                related = {'question': question_objs[i], 'order': j}
                choice_objs.append(ChoiceForm(option, related=related).save())

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


# TODO Tests for MonitoringAssignUpdateView
class MonitoringAssignUpdateView(LoginRequiredMixin, PermissionRequiredMixin, FilterView):
    model = Institution
    filterset_class = InstitutionFilter
    permission_required = 'monitorings.change_monitoring'
    template_name = 'monitorings/institution_assign.html'

    def get_queryset(self, *args, **kwargs):
        qs = super(MonitoringAssignUpdateView, self).get_queryset(*args, **kwargs)
        return qs.exclude(monitorings=self.monitoring.pk).select_related('region')

    @cached_property
    def monitoring(self):
        return get_object_or_404(Monitoring, slug=self.kwargs['slug'])

    def get_context_data(self, *args, **kwargs):
        context = super(MonitoringAssignUpdateView, self).get_context_data(*args, **kwargs)
        context['monitoring'] = self.monitoring
        return context

    def post(self, request, *args, **kwargs):
        ids = request.POST.getlist('to_assign')
        qs = Institution.objects.filter(pk__in=ids).exclude(monitorings=self.monitoring.pk)
        count = 0
        count = len(MonitoringInstitution.objects.bulk_create(
                    MonitoringInstitution(monitoring=self.monitoring,
                                          institution=institution)
                    for institution in qs))
        msg = _("%(count)d institutions was assigned " +
                "to %(monitoring)s") % {'count': count,
                                        'monitoring': self.monitoring}
        messages.success(self.request, msg)
        return HttpResponseRedirect(request.get_full_path())


class MonitoringSignleAssingUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'monitoring/institution_assing_single.html'

    @cached_property
    def monitoring(self):
        return get_object_or_404(Monitoring, slug=self.kwargs['slug'])

    @cached_property
    def institution(self):
        return get_object_or_404(Institution, slug=self.kwargs['institution_slug'])

    def check_thr(self):
        thr = MonitoringInstitution.objects.filter(monitoring=self.monitoring,
                                                   institution=self.institution).first()
        if thr:
            return HttpResponseRedirect(thr.get_absolute_url())
        return None

    def get(self, *args, **kwargs):
        return (self.check_thr() or
                super(MonitoringSignleAssingUpdateView, self).get(*args, **kwargs))

    def post(self, *args, **kwargs):
        thr = self.check_thr()
        if thr:
            return thr
        new_thr = MonitoringInstitution.objects.create(monitoring=self.monitoring,
                                                       institution=self.institution)
        msg = _("Institution %(institution)s assigned to " +
                "monitoring %(monitoring)s") % {'institution': self.institution,
                                                'monitoring': self.monitoring}
        messages.success(self.requests, msg)
        return HttpResponseRedirect(new_thr.get_absolute_url())


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


class SheetCreateView(LoginRequiredMixin, CustomJSONResponseMixin, TemplateView):
    template_name = 'monitorings/monitoring_form_answer.html'

    @cached_property
    def thr(self):
        return get_object_or_404(MonitoringInstitution,
                                 monitoring__slug=self.kwargs['slug'],
                                 institution__slug=self.kwargs['institution_slug'])

    def get_context_data(self, *args, **kwargs):
        context = super(SheetCreateView, self).get_context_data(*args, **kwargs)
        context['monitoring'] = self.thr.monitoring
        context['institution'] = self.thr.institution
        return context

    def get(self, *args, **kwargs):
        if Sheet.objects.filter(monitoring_institution__monitoring=self.thr.monitoring,
                                monitoring_institution__institution=self.thr.institution,
                                user=self.request.user).exists():
            messages.info(self.request, _("Unable to rank once institution twice times."))
            return HttpResponseRedirect(self.thr.monitoring.get_sheet_list_url(self.thr.institution))
        return super(SheetCreateView, self).get(*args, **kwargs)

    @cached_property
    def answer_dict(self):
        return {x['question_id']: x for x in self.data.get('result', [])}

    def get_answer_by_pk(self, pk):
        return self.answer_dict[pk]

    def _construct_answer_forms(self, questions, sheet):
        forms = []
        for question in questions:
            answer = self.get_answer_by_pk(question.pk)
            form_cls = get_form_cls_for_question(question)
            form = form_cls(data=answer, question=question, sheet=sheet)
            forms.append(form)
        return forms

    def post(self, *args, **kwargs):  # TODO: Transactions in MonitoringAnswerView
        self.data = json.loads(self.request.body.decode('utf-8'))

        thr = self.thr
        (monitoring, institution) = (thr.monitoring, thr.institution)

        questions = Question.objects.filter(monitoring=monitoring).all()
        thr = get_object_or_404(MonitoringInstitution, monitoring=monitoring,
                                institution=institution)

        sheet, created = Sheet.objects.get_or_create(monitoring_institution=thr,
                                                     user=self.request.user,
                                                     point=self.data.get('point', 0))

        # Validate one sheet per user
        if not created:
            return self.error(error="Unable to answer twice")

        # Validate all answers
        for question in questions:
            answer = self.get_answer_by_pk(question.pk)
            if not answer:
                return self.error(error="Missing answer for question #%d" % (question.pk))
        # Construct forms
        answer_forms = self._construct_answer_forms(questions, sheet)

        # Validate forms
        if not all(x.is_valid() for x in answer_forms):
            return self.error(errors=[self.error_list(x) for x in answer_forms])

        # Save answers
        [form.save() for form in answer_forms]
        messages.success(self.request, _("Rank saved. Thank you."))
        return JsonResponse({'success': True,
                             'return_url': monitoring.get_institution_url(institution)})


class MonitoringApiDetailView(JSONResponseMixin, DetailView):
    model = Monitoring

    def get_options(self, question):
        for choice in question.choice_set.all():
            yield {'key': choice.key, 'value': choice.value}

    def get_conditions(self, question):
        for condition in question.condition_related.all():
            data = {}
            data['type'] = condition.type
            data['target'] = condition.target.order  # It's ok, "order"
            data['value'] = condition.value
            yield data

    def get_questions(self):
        for question in self.object.question_set.all():
            data = {}
            data['id'] = question.id
            data['name'] = question.name
            data['description'] = question.description
            data['type'] = question.type
            data['hideConditions'] = list(self.get_conditions(question))
            if question.type == Question.TYPE.choice:
                data['options'] = list(self.get_options(question))
            yield data

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {}
        context['name'] = self.object.name
        context['description'] = self.object.description
        context['questions'] = list(self.get_questions())
        return self.render_json_response(context)

    def get_queryset(self, *args, **kwargs):
        qs = super(MonitoringApiDetailView, self).get_queryset(*args, **kwargs)
        return qs.prefetch_related('question_set',
                                   'question_set__condition_related',
                                   'question_set__condition_related__target',
                                   'question_set__choice_set',
                                   )


class MonitoringInstitutionDetailView(SelectRelatedMixin, PrefetchRelatedMixin, ListView):
    template_name = 'monitorings/sheet_list.html'
    model = Sheet
    select_related = ['user', ]
    prefetch_related = ['answer_set',
                        'answer_set__question',
                        'answer_set__answertext',
                        'answer_set__answerchoice']

    @cached_property
    def thr(self):
        qs = MonitoringInstitution.objects.select_related('monitoring', 'institution')
        return get_object_or_404(qs,
                                 monitoring__slug=self.kwargs['slug'],
                                 institution__slug=self.kwargs['institution_slug'])

    def get_queryset(self, *args, **kwargs):
        qs = super(MonitoringInstitutionDetailView, self).get_queryset(*args, **kwargs)
        return qs.filter(monitoring_institution=self.thr)

    def get_context_data(self, *args, **kwargs):
        context = super(MonitoringInstitutionDetailView, self).get_context_data(*args, **kwargs)
        context['monitoring'] = self.thr.monitoring
        context['institution'] = self.thr.institution
        return context
