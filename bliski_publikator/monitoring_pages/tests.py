from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django.test import TestCase

from ..users.factories import UserFactory
from ..monitorings.factories import MonitoringFactory
from .factories import PageFactory
from .models import Page


class PageTestCase(TestCase):
    def setUp(self):
        self.monitoring = MonitoringFactory(name="Monitoring sportowy")
        self.obj = PageFactory(title="Dlaczego?", monitoring=self.monitoring)

    def test_str(self):
        self.assertEqual(force_text(self.obj), "Dlaczego?")

    def test_get_absolute_url(self):
        self.assertEqual(self.obj.get_absolute_url(),
                         "/monitorings/monitoring-sportowy/dlaczego")

    def test_get_update_url(self):
        self.assertEqual(self.obj.get_update_url(),
                         "/monitorings/monitoring-sportowy/dlaczego/~update")

    def test_get_delete_url(self):
        self.assertEqual(self.obj.get_delete_url(),
                         "/monitorings/monitoring-sportowy/dlaczego/~delete")

    def test_get_add_url(self):
        self.assertEqual(Page.get_add_url(self.monitoring),
                         "/monitorings/monitoring-sportowy/~create")


class PageCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.monitoring = MonitoringFactory()
        self.url = reverse('monitorings:pages:create', kwargs={'monitoring_slug': self.monitoring})

    def test_auth(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_status(self):
        self.client.login(username=self.user.username, password='pass')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_permitted(self):
        self.client.login(username=self.user.username, password='pass')
        self.user.assign_perm('monitoring_pages.add_page')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)


class PageUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.obj = PageFactory()
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
        self.user.assign_perm('monitoring_pages.change_page')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)


class PageDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.obj = PageFactory()
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
        self.user.assign_perm('monitoring_pages.delete_page')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
