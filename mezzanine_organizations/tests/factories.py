# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import factory

from django.contrib.auth import get_user_model

from ..models import Organization, OrganizationalUnit

EXAMPLE_DOMAIN = 'org.example.gov'
DEFAULT_PASSWORD = 'defaultpassword'

class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = get_user_model()
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    username = factory.Sequence(lambda n: 'user_%s' % n)
    email = factory.LazyAttribute(lambda o: '{}@{}'.format(o.username,
                                                           EXAMPLE_DOMAIN))
    is_staff = True
    is_active = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.groups.add(group)


class LeaderFactory(UserFactory):
    username = factory.Sequence(lambda n: 'leader_%s' % n)


class MemberFactory(UserFactory):
    username = factory.Sequence(lambda n: 'member_%s' % n)


class AdminFactory(UserFactory):
    username = 'admin'
    password = factory.PostGenerationMethodCall('set_password', 'admin')
    is_superuser = True


class OrganizationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Organization


class ExampleOrganizationFactory(OrganizationFactory):
    title = 'org_example'
    domain = EXAMPLE_DOMAIN


#class Example2x2Organizations(OrganizationalUnit):
#    title = 'org_example'
#    domain = 'org.example.gov'
#
#    def make_ous(self):
#        n_members = 2
#        org_x_level = 2
#        for i in range(0, org_x_level):
#            members = (MemberFactory(
#                username='member_{}_{}'.format(i, mi))
#                for mi in range(0, cls.n_members))


class OrganizationalUnitFactory(factory.DjangoModelFactory):
    FACTORY_FOR = OrganizationalUnit

    organization = factory.SubFactory(OrganizationFactory)
    leader = factory.SubFactory(LeaderFactory)


    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                self.members.add(member)


    #def com