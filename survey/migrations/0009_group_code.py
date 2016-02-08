# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-08 03:55
from __future__ import unicode_literals

from django.db import migrations, models
import survey.utils


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_test_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='code',
            field=models.CharField(default=survey.utils.generate_code, max_length=10, null=True),
        ),
    ]
