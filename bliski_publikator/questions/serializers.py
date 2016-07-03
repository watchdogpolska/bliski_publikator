from rest_framework import serializers
from rest_framework.serializers import HyperlinkedRelatedField
from .models import Answer, AnswerChoice, AnswerText, Choice, Condition, Question, Sheet


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Choice
        fields = ('key', 'value', 'order')


class ConditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Condition
        fields = ('type', 'target', 'related', 'value')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    condition_related = ConditionSerializer(many=True, read_only=True)
    choice_set = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('monitoring',
                  'created_by',
                  'name',
                  'description',
                  'type',
                  'order',
                  'condition_related',
                  'choice_set')


class AnswerTextSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnswerText
        fields = ('value',)


class AnswerChoiceSerializer(serializers.HyperlinkedModelSerializer):
    value = ChoiceSerializer()

    class Meta:
        model = AnswerChoice
        fields = ('value',)


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    value = serializers.CharField(read_only=True)
    answertext = AnswerTextSerializer()
    answerchoice = AnswerChoiceSerializer()

    class Meta:
        model = Answer
        fields = ('question', 'sheet', 'answertext', 'answerchoice', 'value')


class SheetSerializer(serializers.HyperlinkedModelSerializer):
    on_site = serializers.CharField(source='get_sheet_url', read_only=True)
    monitoring = HyperlinkedRelatedField(source='monitoring_institution.monitoring',
                                         view_name='monitoring-detail',
                                         read_only=True)
    institution = HyperlinkedRelatedField(source='monitoring_institution.institution',
                                          view_name='institution-detail',
                                          read_only=True)
    answer_set = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Sheet
        fields = ('on_site',
                  'user',
                  'point',
                  'created',
                  'monitoring',
                  'institution',
                  'answer_set',)
