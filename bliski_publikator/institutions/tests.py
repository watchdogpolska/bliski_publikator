from django.test import TestCase
from django.core.urlresolvers import reverse

from ..users.factories import UserFactory
from .factories import InstitutionFactory
from django.contrib.auth.models import Permission


def assign_perm(perm, user):
    app_label, codename = perm.split('.', 1)
    perm_obj = Permission.objects.get(content_type__app_label=app_label,
                                      codename=codename)
    user.user_permissions.add(perm_obj)


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
