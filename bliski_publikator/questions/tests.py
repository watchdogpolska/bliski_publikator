import django
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from .admin import AnswerAdmin, AnswerChoiceAdmin, AnswerTextAdmin, ChoiceAdmin, QuestionAdmin, SheetAdmin, ConditionAdmin
from .models import Answer, AnswerChoice, AnswerText, Choice, Condition, Question, Sheet


class MixinAdminTestCase(object):
    admin = None
    model = None

    def setUp(self):
        self.site = AdminSite()

    def assertIsValid(self, model_admin, model):  # See django/tests/modeladmin/tests.py#L602
        admin_obj = model_admin(model, self.site)
        if django.VERSION > (1, 9):
            errors = admin_obj.check()
        else:
            errors = admin_obj.check(model)
        expected = []
        self.assertEqual(errors, expected)

    def test_is_valid(self):
        self.assertIsValid(self.admin, self.model)


class QuestionAdminTestCase(MixinAdminTestCase, TestCase):
    admin = QuestionAdmin
    model = Question


class AnswerAdminTestCase(MixinAdminTestCase, TestCase):
    admin = AnswerAdmin
    model = Answer


class AnswerChoiceAdminTestCase(MixinAdminTestCase, TestCase):
    admin = AnswerChoiceAdmin
    model = AnswerChoice


class AnswerTextAdminTestCase(MixinAdminTestCase, TestCase):
    admin = AnswerTextAdmin
    model = AnswerText


class ChoiceAdminTestCase(MixinAdminTestCase, TestCase):
    admin = ChoiceAdmin
    model = Choice


class SheetAdminTestCase(MixinAdminTestCase, TestCase):
    admin = SheetAdmin
    model = Sheet


class ConditionAdminTestCase(MixinAdminTestCase, TestCase):
    admin = ConditionAdmin
    model = Condition
