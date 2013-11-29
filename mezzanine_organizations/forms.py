# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .models import OrganizationalUnit


class MixinUserLabelFromInstance(object):
    def label_from_instance(self, obj):
        label = obj.username
        if obj.last_name and obj.first_name:
            label = u'{} {}'.format(
                obj.last_name, obj.first_name).lower().title()
        if obj.email:
            label += u' - {}'.format(obj.email)
        return label


class UserModelChoiceField(MixinUserLabelFromInstance,
                           forms.ModelChoiceField):
    pass


class UsersModelMultipleChoiceField(MixinUserLabelFromInstance,
                                    forms.ModelMultipleChoiceField):
    pass


class OrganizationalUnitForm(forms.ModelForm):
    _help_text_user_model = _(
        'The "members" field show only users with "email" field is not empty'
        ' and field "is_staff" set to "True".')
    leader = UserModelChoiceField(
        queryset=get_user_model().objects.exclude(email__exact='').exclude(
            is_staff=False).order_by('last_name', 'first_name'),
        required=False,
        help_text=_help_text_user_model)
    members = UsersModelMultipleChoiceField(
        queryset=get_user_model().objects.exclude(email__exact='').exclude(
            is_staff=False).order_by('last_name', 'first_name'),
        widget=FilteredSelectMultiple(_('Members'), False, attrs={}),
        required=False,
        help_text=_help_text_user_model)

    class Meta:
        model = OrganizationalUnit