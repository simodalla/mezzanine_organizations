#!/usr/bin/env python
import os
import sys


os.environ['DJANGO_SETTINGS_MODULE'] = 'project_template.settings'
project_template_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'project_template')
sys.path.insert(0, project_template_dir)

from django.test.utils import get_runner
from django.conf import settings


def runtests(tests=('mezzanine_organizations',)):
    """
    Takes a list as first argument, enumerating the apps and specific testcases
    that should be executed. The syntax is the same as for what you would pass
    to the ``django-admin.py test`` command.

    Examples::

        # run the default test suite
        runtests()

        # only run the tests from application ``mezzanine_organizations``
        runtests(['mezzanine_organizations'])

        # only run testcase class ``UnauthorizedListPagesPageAuthGroupTest``
        # from app ``mezzanine_organizations``
        runtests(['mezzanine_organizations.UnauthorizedListPagesPageAuthGroupTest'])

        # run all tests from application ``mezzanine_page_auth`` and the test
        # named ``test_register`` on the
        # ``mezzanine_organizations.UnauthorizedListPagesPageAuthGroupTest``
        # testcase.
        runtests(['mezzanine_organizations.UnauthorizedListPagesPageAuthGroupTest.
        test_unauthorized_list_pages_with_user_with_one_group''])
    """
    #print(settings.TEST_RUNNER)
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(tests)
    sys.exit(bool(failures))

#def runtests():
#
#    #import os, sys, shutil, atexit
#    from mezzanine.utils.importing import path_for_import
#
#    #os.environ["DJANGO_SETTINGS_MODULE"] = "project_template.settings"
#    mezz_path = path_for_import("mezzanine")
#    #project_path = os.path.join(mezz_path, "project_template")
#    #local_settings_path = os.path.join(project_path, "local_settings.py")
#
#    sys.path.insert(0, mezz_path)
#    #sys.path.insert(0, project_path)
#
##    if not os.path.exists(local_settings_path):
##        shutil.copy(local_settings_path + ".template", local_settings_path)
##        with open(local_settings_path, "a") as f:
##            f.write("""
##
##INSTALLED_APPS = (
##    "django.contrib.admin",
##    "django.contrib.auth",
##    "django.contrib.contenttypes",
##    "django.contrib.redirects",
##    "django.contrib.sessions",
##    "django.contrib.sites",
##    "django.contrib.sitemaps",
##    "django.contrib.staticfiles",
##    "mezzanine.boot",
##    "mezzanine.conf",
##    "mezzanine.core",
##    "mezzanine.generic",
##    "mezzanine.blog",
##    "mezzanine.forms",
##    "mezzanine.pages",
##    "mezzanine.galleries",
##    "mezzanine.twitter",
##    "mezzanine.accounts",
##    "mezzanine.mobile",
##)
##
##                """)
##        atexit.register(lambda: os.remove(local_settings_path))
#
#    from django.core.management.commands import test
#    print("*******************")
#    sys.exit(test.Command().execute(verbosity=1))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        tests = sys.argv[1:]
        runtests(tests)
    else:
        runtests()