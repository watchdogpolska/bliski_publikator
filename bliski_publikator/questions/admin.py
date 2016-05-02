from django.contrib import admin
from django.utils.encoding import force_text

from .models import Question, Answer, AnswerChoice, AnswerText, Choice, Sheet, Condition


class ConditionInline(admin.TabularInline):
    '''
        Stacked Inline View for Condition
    '''
    model = Condition
    fk_name = 'related'


class ChoiceInline(admin.TabularInline):
    '''
        Tabular Inline View for Choice
    '''
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    '''
        Admin View for Question
    '''
    list_display = ('name', 'type', 'monitoring', 'created_by', 'order', 'display_choices')
    list_filter = ('monitoring',)
    inlines = [
        ConditionInline,
        ChoiceInline
    ]

    def display_choices(self, obj):
        return ', '.join(force_text(x) for x in obj.choice_set.all())

    def get_queryset(self, *args, **kwargs):
        qs = super(QuestionAdmin, self).get_queryset(*args, **kwargs)
        return qs.prefetch_related('choice_set')


admin.site.register(Question, QuestionAdmin)


class AnswerChoiceInline(admin.StackedInline):
    '''
        Stacked Inline View for AnswerChice
    '''
    model = AnswerChoice


class AnswerTextInline(admin.StackedInline):
    '''
        Stacked Inline View for AnswerText
    '''
    model = AnswerText


class AnswerAdmin(admin.ModelAdmin):
    '''
        Admin View for Answer
    '''
    list_display = ('pk', 'question', 'sheet', 'sheet__user')
    list_filter = ('sheet__monitoring', )
    inlines = [
        AnswerChoiceInline,
        AnswerTextInline
    ]

    def sheet__user(self, obj):
        return obj.sheet.user

    def get_queryset(self, *args, **kwargs):
        qs = super(AnswerAdmin, self).get_queryset(*args, **kwargs)
        return qs.select_related('sheet__user', 'question')


admin.site.register(Answer, AnswerAdmin)


class AnswerChoiceAdmin(admin.ModelAdmin):
    '''
        Admin View for AnswerChoice
    '''
    list_display = ('pk', 'answer', 'answer__sheet__monitoring', 'answer__question', 'value',)
    list_filter = ('answer__sheet__monitoring', 'answer__question')

    def answer__sheet__monitoring(self, obj):
        return obj.answer.sheet.monitoring

    def answer__question(self, obj):
        return obj.answer.question

    def get_queryset(self, *args, **kwargs):
        qs = super(AnswerChoiceAdmin, self).get_queryset(*args, **kwargs)
        return qs.select_related('answer__question', 'answer__sheet__monitoring')

admin.site.register(AnswerChoice, AnswerChoiceAdmin)


class AnswerTextAdmin(admin.ModelAdmin):
    '''
        Admin View for AnswerText
    '''
    list_display = ('answer', 'value',)
    list_filter = ('answer__sheet__monitoring', 'answer__question')
    search_fields = ('value', )

admin.site.register(AnswerText, AnswerTextAdmin)


class AnswerChoiceInline(admin.StackedInline):
    '''
        Stacked Inline View for AnswerChoice
    '''
    model = AnswerChoice


class ChoiceAdmin(admin.ModelAdmin):
    '''
        Admin View for Choice
    '''
    list_display = ('key', 'value', 'question')
    list_filter = ('question', 'question__monitoring')

admin.site.register(Choice, ChoiceAdmin)


class AnswerInline(admin.StackedInline):
    '''
        Stacked Inline View for Answer
    '''
    model = Answer


class SheetAdmin(admin.ModelAdmin):
    '''
        Admin View for Sheet
    '''
    list_display = ('monitoring', 'user')
    list_filter = ('monitoring',)
    inlines = [
        AnswerInline,
    ]

admin.site.register(Sheet, SheetAdmin)


class ConditionAdmin(admin.ModelAdmin):
    '''
        Admin View for Condition
    '''
    list_display = ('type', 'target', 'related')
    list_filter = ('type', 'target', 'related', 'related__monitoring')

admin.site.register(Condition, ConditionAdmin)
