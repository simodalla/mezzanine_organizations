# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.pages.admin import PageAdmin, RichTextPage

from .models import Organization, OrganizationalUnit
from .forms import OrganizationalUnitForm


class OrganizationAdmin(PageAdmin):
    fieldsets = (deepcopy(PageAdmin.fieldsets) +
                 ((_("Organization Data"), {"fields": ("domain",)}),))

class OrganizationalUnitAdmin(PageAdmin):
    fieldsets = (deepcopy(PageAdmin.fieldsets) +
                 ((_("Organizational Unit Data"),
                   {"fields": ("organization", "leader", "members",
                               "email", "pec", "phone_number", "fax",
                               "location")}),))
    form = OrganizationalUnitForm

    def save_model(self, request, obj, form, change):
        print(obj)
        super(OrganizationalUnitAdmin, self).save_model(
            request, obj, form, change)
        #print(obj)


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationalUnit, OrganizationalUnitAdmin)
