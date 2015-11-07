#!/usr/bin/env python

from setuptools import setup

setup(
    name='App',
    version='1.0',
    zip_safe=True,
    description='App',
    author='Micwaits Microcood',
    author_email='microcood@gmial.com',
    install_requires=[
        'Django',
        'python-docx',
        'pytz',
        'lxml',
        'django-tracking2',
        'Unidecode',
    ],
)
