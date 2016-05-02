# -*- coding: utf-8 -*-
from braces.forms import UserKwargModelFormMixin
from django import forms

from .models import Choice, Condition, Question


class RelatedInstanceMixin(object):
    def __init__(self, *args, **kwargs):
        related = kwargs.pop('related', {})
        super(RelatedInstanceMixin, self).__init__(*args, **kwargs)
        for key, value in related.items():
            setattr(self.instance, key, value)


class QuestionForm(UserKwargModelFormMixin, RelatedInstanceMixin, forms.ModelForm):
    class Meta:
        model = Question
        fields = ['name', 'description', 'type']


class ChoiceForm(RelatedInstanceMixin, forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['key', 'value']


class ConditionForm(RelatedInstanceMixin, forms.ModelForm):
    class Meta:
        model = Condition
        fields = ['type']
