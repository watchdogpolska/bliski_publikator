from __future__ import unicode_literals

import django
from django.contrib.admin.sites import AdminSite
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.encoding import force_text

from ..users.factories import UserFactory
from ..monitorings.factories import MonitoringFactory
from .factories import InstitutionFactory
from .models import Institution
from .admin import InstitutionAdmin
from .forms import InstitutionForm
from ..teryt.factories import JSTFactory


class InstitutionTestCase(TestCase):
    def setUp(self):
        self.obj = InstitutionFactory(name="WSA w Warszawie")

    def test_str(self):
        self.assertEqual(force_text(self.obj), "WSA w Warszawie")

    def test_get_absolute_url(self):
        self.assertEqual(self.obj.get_absolute_url(),
                         "/institutions/institution-wsa-w-warszawie")

    def test_get_update_url(self):
        self.assertEqual(self.obj.get_update_url(),
                         "/institutions/institution-wsa-w-warszawie/~update")

    def test_get_delete_url(self):
        self.assertEqual(self.obj.get_delete_url(),
                         "/institutions/institution-wsa-w-warszawie/~delete")

    def test_get_add_url(self):
        self.assertEqual(Institution.get_add_url(),
                         "/institutions/~create")


class InstitutionListViewTestCase(TestCase):
    def test_status(self):
        resp = self.client.get(reverse('institutions:list'))
        self.assertEqual(resp.status_code, 200)


class InstitutionDetailViewTestCase(TestCase):
    def setUp(self):
        self.institution = InstitutionFactory()
        self.url = self.institution.get_absolute_url()

    def test_status(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)


class InstitutionCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('institutions:create')

    def test_auth(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_status(self):
        self.client.login(username=self.user.username, password='pass')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_permitted(self):
        self.client.login(username=self.user.username, password='pass')
        self.user.assign_perm('institutions.add_institution')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)


class InstitutionUpdateViewTestCase(TestCase):
    def setUp(self):
        self.institution = InstitutionFactory()
        self.user = UserFactory()
        self.url = self.institution.get_update_url()

    def test_auth(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_status(self):
        self.client.login(username=self.user.username, password='pass')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_permitted(self):
        self.client.login(username=self.user.username, password='pass')
        self.user.assign_perm('institutions.change_institution')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)


class InstitutionDeleteViewTestCase(TestCase):
    def setUp(self):
        self.institution = InstitutionFactory()
        self.user = UserFactory()
        self.url = self.institution.get_delete_url()

    def test_auth(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_status(self):
        self.client.login(username=self.user.username, password='pass')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_permitted(self):
        self.client.login(username=self.user.username, password='pass')
        self.user.assign_perm('institutions.delete_institution')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)


class InstitutionAutocompleteTestCase(TestCase):
    def setUp(self):
        self.institution = InstitutionFactory()

    def test_status(self):
        resp = self.client.get(reverse('institutions:autocomplete'))
        self.assertEqual(resp.status_code, 200)


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


class InstitutionAdminTestCase(MixinAdminTestCase, TestCase):
    admin = InstitutionAdmin
    model = Institution


class InstitutionFormTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.instance = InstitutionFactory()
        self.monitoring_A = MonitoringFactory()
        self.monitoring_B = MonitoringFactory()
        self.monitoring_C = MonitoringFactory()

    def test_update_monitorings(self):
        """
        Regression test for watchdogpolska/bliski_publikator#55
        """
        data = {'name': 'X', 'regon': 'X', 'krs': 'X', 'region': JSTFactory(category__level=3).pk}

        form = InstitutionForm(data=data, user=self.user, instance=self.instance)
        self.assertEqual(form.is_valid(), True, repr(form.errors))
        self.assertQuerysetEqual(self.instance.monitorings.all(), [])

        data['monitorings'] = [self.monitoring_A.pk, self.monitoring_B.pk]

        form = InstitutionForm(data=data, user=self.user, instance=self.instance)
        self.assertEqual(form.is_valid(), True, repr(form.errors))
        form.save()
        self.assertQuerysetEqual(self.instance.monitorings.all(),
                                 [repr(self.monitoring_A), repr(self.monitoring_B)],
                                 ordered=False)

        data['monitorings'] = [self.monitoring_B.pk, self.monitoring_C.pk]

        form = InstitutionForm(data=data, user=self.user, instance=self.instance)
        self.assertEqual(form.is_valid(), True, repr(form.errors))
        form.save()
        self.assertQuerysetEqual(self.instance.monitorings.all(),
                                 [repr(self.monitoring_B), repr(self.monitoring_C)],
                                 ordered=False)
