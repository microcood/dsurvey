# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_auto_20151029_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresponse',
            name='examination',
            field=models.ForeignKey(to='survey.Examination', default=0),
            preserve_default=False,
        ),
    ]
