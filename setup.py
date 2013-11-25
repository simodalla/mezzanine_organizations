# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

README = open(os.path.join(
    os.path.dirname(__file__), 'README.rst')).read().decode('utf-8')

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    "mezzanine >= 1.3.0",
]

from mezzanine_organizations import __version__ as version

setup(
    name='mezzanine-organizations',
    version=version,
    author='Simone Dalla',
    author_email='simodalla@gmail.com',
    description='A Mezzanine module for manage organizations.',
    long_description=README,
    license='BSD License',
    url='https://github.com/simodalla/mezzanine_organizations/',
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    test_suite="runtests.runtests",
    tests_require=["mock", "pep8", "factory_boy"],
    classifiers=[
        'Development Status :: 5 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
