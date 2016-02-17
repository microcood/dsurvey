#!/usr/bin/env python

from setuptools import setup

setup(
    name='App',
    version='1.0',
    zip_safe=True,
    description='App',
    author='Micwaits Microcood',
    author_email='microcood@gmail.com',
    install_requires=[
        'Django>1.8',
        'python-docx',
        'pytz',
        'lxml',
        'xlsxwriter',
        'django-tracking2',
        'Unidecode',
    ],
)
