# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from copy import deepcopy

from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import Page

from .models import Organization, OrganizationalUnit
from .forms import OrganizationalUnitForm


class OrganizationAdmin(PageAdmin):
    fieldsets = (deepcopy(PageAdmin.fieldsets) +
                 ((_("Organization Data"), {"fields": ("domain",)}),))


class OrganizationalUnitAdmin(PageAdmin):
    fieldsets = (deepcopy(PageAdmin.fieldsets) +
                 ((_("Organizational Unit Data"),
                   {"fields": ("leader", "members", "email", "pec",
                               "phone_number", "fax", "location")}),))
    form = OrganizationalUnitForm

    def add_view(self, request, **kwargs):
        changelist_view = 'admin:{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.module_name)
        parent = request.GET.get('parent', None)
        if not parent:
            self.message_user(
                request,
                _("Is not possible add an '%(object_type)s' as root page.") % {
                    'object_type': self.model._meta.verbose_name},
                level=messages.ERROR)
            return redirect(changelist_view)
        try:
            parent = Page.objects.get(pk=parent)
            modules_ok = [m._meta.module_name for m in [OrganizationalUnit,
                                                        Organization]]
            if parent.content_model not in modules_ok:
                self.message_user(
                    request,
                    _("Is not possible add an '%(obj_type)s' under a page"
                      " unlike from '%(obj_parent_type)s' type.") % {
                        'obj_type': self.model._meta.verbose_name,
                        'obj_parent_type': Organization._meta.verbose_name},
                    level=messages.ERROR)
                return redirect(changelist_view)

        except Page.DoesNotExist:
            self.message_user(
                request, _("The parent page not exist."), level=messages.ERROR)
            return redirect(changelist_view)

        return super(OrganizationalUnitAdmin, self).add_view(request, **kwargs)

    def change_view(self, request, object_id, **kwargs):
        #print(request)
        return super(OrganizationalUnitAdmin, self).change_view(
            request, object_id, **kwargs)


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationalUnit, OrganizationalUnitAdmin)
