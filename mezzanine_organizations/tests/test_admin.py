# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.messages import ERROR as error_message
from django.core.urlresolvers import reverse
from django.test import TestCase

from mezzanine.pages.models import RichTextPage

from .factories import *
from ..models import OrganizationalUnit


class AddChangeViewAdminTest(TestCase):
    @classmethod
    def setUpClass(cls):
        OrganizationFactory(title='super')
        cls.org = ExampleOrganizationFactory()
        cls.n_members = 2
        cls.org_x_level = 2
        for i in range(0, cls.org_x_level):
            members = (UserFactory(
                username='member_{}_{}'.format(i, mi))
                       for mi in range(0, cls.n_members))
            ou = OrganizationalUnitFactory.create(
                title='ou_{}'.format(i), organization=cls.org, parent=cls.org,
                members=members,
            )
            for j in range(0, cls.org_x_level):
                members = (UserFactory(
                    username='member_{}_{}_{}'.format(i, j, mj))
                           for mj in range(0, cls.n_members))
                OrganizationalUnitFactory.create(
                    title='ou_{}_{}'.format(i, j), organization=cls.org,
                    members=members,
                    parent=ou)
        cls.admin = AdminFactory()
        cls.add_view = (
            'admin:{}_{}_add'.format(
                OrganizationalUnit._meta.app_label,
                OrganizationalUnit._meta.module_name))
        cls.changelist_view = (
            'admin:{}_{}_changelist'.format(
                OrganizationalUnit._meta.app_label,
                OrganizationalUnit._meta.module_name))

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()
        OrganizationalUnit.objects.all().delete()
        Organization.objects.all().delete()

    def setUp(self):
        self.client.login(username=self.admin.username,
                          password=self.admin.username)

    def test_add_view_without_parent(self):
        """
        Test that the call of admin add_view for add a new "OrganizationalUnit"
        without "parent" into query url, redirect to admin changelist view
        with a error message.
        """
        response = self.client.get(reverse(self.add_view), follow=True)
        self.assertRedirects(response, reverse('admin:pages_page_changelist'))
        self.assertIn(
            ('http://testserver' + reverse(self.changelist_view), 302,),
            response.redirect_chain)
        msgs = [(m.message, m.level) for m in response.context['messages']]
        self.assertIn(
            ("Is not possible add an '{}' as root page.".format(
                OrganizationalUnit._meta.verbose_name), error_message), msgs)

    def test_add_view_parent_not_exist(self):
        """
        Test that the call of admin add_view for add a new "OrganizationalUnit"
        with "parent" into query url that isn't pk in db, redirect to admin
        changelist view with a error message.
        """
        response = self.client.get(
            reverse(self.add_view) + '?parent={}'.format(
                OrganizationalUnit.objects.latest().pk+10),
            follow=True)
        self.assertRedirects(response, reverse('admin:pages_page_changelist'))
        self.assertIn(
            ('http://testserver' + reverse(self.changelist_view), 302,),
            response.redirect_chain)
        msgs = [(m.message, m.level) for m in response.context['messages']]
        self.assertIn(("The parent page not exist.", error_message), msgs)

    def test_add_view_parent_unlike_from_organization(self):
        """
        Test that the call of admin add_view for add a new "OrganizationalUnit"
        with "parent" into query url that is a RichTextPage, unlike from
        Organization, redirect to admin changelist view with a error message.
        """
        response = self.client.get(
            reverse(self.add_view) + '?parent={}'.format(
                RichTextPage.objects.create(title='fake_page').pk),
            follow=True)
        self.assertRedirects(response, reverse('admin:pages_page_changelist'))
        self.assertIn(
            ('http://testserver' + reverse(self.changelist_view), 302,),
            response.redirect_chain)
        msgs = [(m.message, m.level) for m in response.context['messages']]
        self.assertIn(
            ("Is not possible add an '%(obj_type)s' under a page unlike from"
             " '%(obj_parent_type)s' type." % {
                'obj_type': OrganizationalUnit._meta.verbose_name,
                'obj_parent_type': Organization._meta.verbose_name},
             error_message), msgs)

    def test_add_view_ok(self):
        """
        Test that the call of admin add_view for add a new "OrganizationalUnit"
        without "parent" into query url, redirect to admin changelist view
        with a error message.
        """
        response = self.client.get(
            reverse(self.add_view) + '?parent={}'.format(self.org.pk),
            follow=True)


