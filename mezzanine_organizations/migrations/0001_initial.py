# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='pages.Page')),
                ('domain', models.CharField(blank=True, null=True, verbose_name='Domain', unique=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
                'ordering': ('_order',),
            },
            bases=('pages.page',),
        ),
        migrations.CreateModel(
            name='OrganizationalUnit',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='pages.Page')),
                ('email', models.EmailField(blank=True, verbose_name='Email', max_length=75)),
                ('pec', models.EmailField(blank=True, verbose_name='Pec', max_length=75)),
                ('phone_number', models.CharField(blank=True, verbose_name='Phone Number', max_length=20)),
                ('fax', models.CharField(blank=True, verbose_name='Fax', max_length=20)),
                ('location', mezzanine.core.fields.RichTextField(blank=True, verbose_name='Location')),
                ('leader', models.ForeignKey(blank=True, verbose_name='Leader', related_name='leader_of', to=settings.AUTH_USER_MODEL, null=True)),
                ('members', models.ManyToManyField(blank=True, null=True, verbose_name='Members', to=settings.AUTH_USER_MODEL, related_name='member_of')),
            ],
            options={
                'get_latest_by': 'created',
                'verbose_name': 'Organizational unit',
                'verbose_name_plural': 'Organizational units',
                'ordering': ('_order',),
            },
            bases=('pages.page',),
        ),
    ]
