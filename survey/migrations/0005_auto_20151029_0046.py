# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='examinee',
            name='first_name',
            field=models.CharField(max_length=100, default='dumb'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examinee',
            name='last_name',
            field=models.CharField(max_length=100, default='diusaldkfjl'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examinee',
            name='middle_name',
            field=models.CharField(max_length=100, default='diummy'),
            preserve_default=False,
        ),
    ]
