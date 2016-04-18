from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django.test import TestCase

from ..users.factories import UserFactory
from .factories import MonitoringFactory
from .models import Monitoring


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

    def test_get_add_url(self):
        self.assertEqual(Monitoring.get_add_url(),
                         "/monitorings/~create")


class MonitoringCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
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
