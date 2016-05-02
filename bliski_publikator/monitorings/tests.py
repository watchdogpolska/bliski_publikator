from __future__ import unicode_literals
from os.path import dirname, join
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django.test import TestCase

from ..users.factories import UserFactory
from .factories import MonitoringFactory
from .models import Monitoring
from ..institutions.factories import InstitutionFactory
from ..questions.models import Answer, Sheet, Question, Choice


class FixtureMixin(object):
    def _get_json(self, filename):
        path = join(dirname(__file__), 'fixtures', filename)
        fp = open(path, 'rb')
        return fp.read()

    def _post_fixture(self, fixture_name, url=None):
        body = self._get_json(fixture_name + '.json')
        return self.client.post(url or self.url, body, content_type="application/json")


class MonitoringTestCase(TestCase):
    def setUp(self):
        self.obj = MonitoringFactory(name="Monitoring sportowy")

    def test_str(self):
        self.assertEqual(force_text(self.obj), "Monitoring sportowy")

    def test_get_absolute_url(self):
        self.assertEqual(self.obj.get_absolute_url(),
                         "/monitorings/monitoring-sportowy")

    def test_get_update_url(self):
        self.assertEqual(self.obj.get_update_url(),
                         "/monitorings/monitoring-sportowy/~update")

    def test_get_delete_url(self):
        self.assertEqual(self.obj.get_delete_url(),
                         "/monitorings/monitoring-sportowy/~delete")

    def test_get_assign_url(self):
        self.assertEqual(self.obj.get_assign_url(),
                         "/monitorings/monitoring-sportowy/~assign")

    def test_get_add_url(self):
        self.assertEqual(Monitoring.get_add_url(),
                         "/monitorings/~create")

    def test_get_answer_url(self):
        institution = InstitutionFactory(name="WSA")
        self.assertEqual(self.obj.get_answer_url(institution),
                         "/monitorings/monitoring-sportowy/wsa/~answer")


class MonitoringCreateViewTestCase(FixtureMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.institution = InstitutionFactory(pk=1)
        self.url = reverse('monitorings:create')

    def test_auth(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_status(self):
        self.client.login(username=self.user.username, password='pass')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_permitted(self):
        self.client.login(username=self.user.username, password='pass')
        self.user.assign_perm('monitorings.add_monitoring')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_basic_fixture(self):
        self.client.login(username=self.user.username, password='pass')
        self.user.assign_perm('monitorings.add_monitoring')
        resp = self._post_fixture('monitoring_basic')
        self.assertEqual(resp.status_code, 200)

    def test_advanced_fixture(self):
        self.client.login(username=self.user.username, password='pass')
        self.user.assign_perm('monitorings.add_monitoring')
        resp = self._post_fixture('monitoring_advanced')
        self.assertEqual(resp.status_code, 200)

    def test_broken_target(self):
        self.client.login(username=self.user.username, password='pass')
        self.user.assign_perm('monitorings.add_monitoring')
        resp = self._post_fixture('monitoring_broken_target')
        self.assertEqual(resp.status_code, 400)


class MonitoringUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.obj = MonitoringFactory()
        self.url = self.obj.get_update_url()

    def test_auth(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_status(self):
        self.client.login(username=self.user.username, password='pass')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_permitted(self):
        self.client.login(username=self.user.username, password='pass')
        self.user.assign_perm('monitorings.change_monitoring')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)


class MonitoringDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.obj = MonitoringFactory()
        self.url = self.obj.get_delete_url()

    def test_auth(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_status(self):
        self.client.login(username=self.user.username, password='pass')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_permitted(self):
        self.client.login(username=self.user.username, password='pass')
        self.user.assign_perm('monitorings.delete_monitoring')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)


class MonitoringAutocompleteTestCase(TestCase):
    def setUp(self):
        self.obj = MonitoringFactory()
        self.url = reverse('monitorings:autocomplete')

    def test_status(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_filter(self):
        resp = self.client.get(self.url, {'q': self.obj.name})
        self.assertContains(resp, self.obj.name)

        resp = self.client.get(self.url, {'q': self.obj.name+"filtered"})
        self.assertNotContains(resp, self.obj.name)


class MonitoringAnswerViewTestCase(FixtureMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.monitoring = MonitoringFactory()
        self.institution = InstitutionFactory()
        self.monitoring.institutions.add(self.institution)
        # self.monitoring.institutions.save()
        self.url = self.monitoring.get_answer_url(self.institution)
        self.short_text_q = Question.objects.create(pk=1,
                                                    type=Question.TYPE.short_text,
                                                    name="Short text question",
                                                    monitoring=self.monitoring,
                                                    created_by=self.user,
                                                    order=0)
        self.long_text_q = Question.objects.create(pk=2,
                                                   type=Question.TYPE.long_text,
                                                   name="Long text question",
                                                   monitoring=self.monitoring,
                                                   created_by=self.user,
                                                   order=1)
        self.long_text_q = Question.objects.create(pk=3,
                                                   type=Question.TYPE.choice,
                                                   name="Choicetext question",
                                                   monitoring=self.monitoring,
                                                   created_by=self.user,
                                                   order=2)
        self.choice = Choice.objects.create(question=self.long_text_q,
                                            key="key",
                                            value="Value of choice",
                                            order=0)

    def test_auth(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_status(self):
        self.client.login(username=self.user.username, password='pass')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_answer_pass(self):
        self.client.login(username=self.user.username, password='pass')
        resp = self._post_fixture('answer_basic')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Answer.objects.count(), 3)
        self.assertTrue(Sheet.objects.filter(monitoring=self.monitoring,
                                             user=self.user).exists())
