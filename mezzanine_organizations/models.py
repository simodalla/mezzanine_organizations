# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import RichTextField
from mezzanine.pages.models import Page


class Organization(Page):
    domain = models.CharField(max_length=100, verbose_name=_('Domain'),
                              blank=True, null=True, unique=True)

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')

    #def get_absolute_url(self):
    #    # TODO: sistemare questo metodo dopo aver sistemato il file urls.py
    #    return '.'


class OrganizationalUnit(Page):
    organization = models.ForeignKey(Organization,
                                     verbose_name=_('Organization'),
                                     related_name='ous')
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                               related_name='leader_of',
                               verbose_name=_('Leader'))
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     blank=True, null=True,
                                     related_name='member_of',
                                     verbose_name=_('Members'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    pec = models.EmailField(blank=True, verbose_name=_('Pec'))
    phone_number = models.CharField(max_length=20, blank=True,
                                    verbose_name=_('Phone Number'))
    fax = models.CharField(max_length=20, blank=True, verbose_name=_('Fax'))
    location = RichTextField(blank=True, verbose_name=_('Location'))

    class Meta:
        verbose_name = _('Organization unit')
        verbose_name_plural = _('Organization units')

    #def get_absolute_url(self):
    #    # TODO: sistemare questo metodo dopo aver sistemato il file urls.py
    #    return '.'

