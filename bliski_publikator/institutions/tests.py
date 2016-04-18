from __future__ import unicode_literals

from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django.test import TestCase

from ..users.factories import UserFactory
from .factories import InstitutionFactory
from .models import Institution


def assign_perm(perm, user):
    app_label, codename = perm.split('.', 1)
    perm_obj = Permission.objects.get(content_type__app_label=app_label,
                                      codename=codename)
    user.user_permissions.add(perm_obj)


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
        assign_perm('institutions.add_institution', self.user)
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
        assign_perm('institutions.change_institution', self.user)
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
        assign_perm('institutions.delete_institution', self.user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)


class InstitutionAutocompleteTestCase(TestCase):
    def setUp(self):
        self.institution = InstitutionFactory()

    def test_status(self):
        resp = self.client.get(reverse('institutions:autocomplete'))
        self.assertEqual(resp.status_code, 200)
