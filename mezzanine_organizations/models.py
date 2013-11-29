# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import RichTextField
from mezzanine.pages.models import Page


class Organization(Page):
    domain = models.CharField(max_length=100, verbose_name=_("Domain"),
                              blank=True, null=True, unique=True)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")


class OrganizationalUnit(Page):
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                               related_name="leader_of",
                               verbose_name=_("Leader"))
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     blank=True, null=True,
                                     related_name="member_of",
                                     verbose_name=_("Members"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    pec = models.EmailField(blank=True, verbose_name=_("Pec"))
    phone_number = models.CharField(max_length=20, blank=True,
                                    verbose_name=_("Phone Number"))
    fax = models.CharField(max_length=20, blank=True, verbose_name=_("Fax"))
    location = RichTextField(blank=True, verbose_name=_("Location"))

    class Meta:
        get_latest_by = "created"
        verbose_name = _("Organizational unit")
        verbose_name_plural = _("Organizational units")

    def get_organization(self, from_down=True):
        ascendats = self.get_ascendants()
        if not from_down:
            ascendats = reversed(ascendats)
        for page in ascendats:
            if isinstance(page, Organization):
                return page.organizarion
            continue
