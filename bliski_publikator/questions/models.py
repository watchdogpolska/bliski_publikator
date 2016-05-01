from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel

from ..monitorings.models import Monitoring


class QuestionQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Question(TimeStampedModel):
    TYPE = Choices((0, 'short_text', _('Short text answer')),
                   (1, 'long_text', _('Long text answer')),
                   (2, 'choice', _("Choice answer")))
    monitoring = models.ForeignKey(to=Monitoring,
                                   verbose_name=_("Monitoring"))
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                   verbose_name=_("Created by"))
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    description = models.TextField(verbose_name=_("Description"))
    type = models.IntegerField(choices=TYPE,
                               default=TYPE.short_text,
                               verbose_name=_("Answer type"))
    order = models.PositiveSmallIntegerField(verbose_name=_("Order"))

    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['order', 'created', ]

    def __str__(self):
        return self.title


class ChoiceQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Choice(TimeStampedModel):
    question = models.ForeignKey(to=Question,
                                 verbose_name=_("Question"))
    value = models.CharField(max_length=50, verbose_name=_("Value"))
    order = models.PositiveSmallIntegerField(verbose_name=_("Order"))

    objects = ChoiceQuerySet.as_manager()

    class Meta:
        verbose_name = _("choice")
        verbose_name_plural = _("choices")
        ordering = ['order', 'created', ]

    def __str__(self):
        return self.value


class ConditionQuerySet(models.QuerySet):
    pass


class Condition(TimeStampedModel):
    TYPE = Choices((0, 'is_true', _('Is true')),
                   (1, 'is_false', _('Is false')),
                   (2, 'is_equal', _("Is equal")),
                   (3, 'is_not_equal', _("Is not equal")),
                   )
    type = models.IntegerField(choices=TYPE,
                               default=TYPE.is_true,
                               verbose_name=_("Answer type"))
    target = models.ForeignKey(to=Question,
                               related_name="condition_target",
                               verbose_name=_("Target"))
    related = models.ForeignKey(to=Question,
                                related_name="condition_related",
                                null=True,
                                blank=True,
                                verbose_name=_("Related"))
    objects = ConditionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Condition")
        verbose_name_plural = _("Conditions")
        ordering = ['created', ]


class SheetQuerySet(models.QuerySet):
    pass


class Sheet(TimeStampedModel):
    monitoring = models.ForeignKey(Monitoring,
                                   verbose_name=_("Monitoring"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_("User"))
    objects = SheetQuerySet.as_manager()

    class Meta:
        verbose_name = _("Sheet")
        verbose_name_plural = _("Sheets")
        ordering = ['monitoring', 'user', 'created', ]


class AnswerQuerySet(models.QuerySet):
    pass


class Answer(TimeStampedModel):
    sheet = models.ForeignKey(to=Sheet,
                              verbose_name=_("Sheet"))
    objects = AnswerQuerySet.as_manager()

    def type(self):
        if self.answertext:
            return 1
        if self.answerdate:
            return 2
        if self.answerbool:
            return 3

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")


class AnswerTextQuerySet(models.QuerySet):
    pass


class AnswerText(TimeStampedModel):
    sheet = models.ForeignKey(to=Sheet,
                              verbose_name=_("Sheet"))
    value = models.CharField(verbose_name=_("Value"), max_length=150)
    objects = AnswerTextQuerySet.as_manager()

    class Meta:
        verbose_name = _("Text answer")
        verbose_name_plural = _("Text answers")


class AnswerDateQuerySet(models.QuerySet):
    pass


class AnswerDate(TimeStampedModel):
    sheet = models.ForeignKey(to=Sheet,
                              verbose_name=_("Sheet"))
    value = models.DateTimeField(verbose_name=_("Value"))

    objects = AnswerTextQuerySet.as_manager()

    class Meta:
        verbose_name = _("Date answer")
        verbose_name_plural = _("Date answers")


class AnswerBoolQuerySet(models.QuerySet):
    pass


class AnswerBool(TimeStampedModel):
    sheet = models.ForeignKey(to=Sheet,
                              verbose_name=_("Sheet"))
    value = models.BooleanField(verbose_name=_("Value"))

    class Meta:
        verbose_name = _("Bool answer")
        verbose_name_plural = _("Bool answers")
