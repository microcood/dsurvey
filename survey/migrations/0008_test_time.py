# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_auto_20151107_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='time',
            field=models.IntegerField(verbose_name='Время', default=3000),
        ),
    ]
