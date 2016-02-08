# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-08 03:56
from __future__ import unicode_literals

from django.db import migrations
from survey.utils import generate_code


def gen_codes(apps, schema_editor):
    Group = apps.get_model('survey', 'Group')
    for group in Group.objects.all():
        group.code = generate_code()
        group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0009_group_code'),
    ]

    operations = [
        migrations.RunPython(gen_codes, reverse_code=migrations.RunPython.noop)
    ]
