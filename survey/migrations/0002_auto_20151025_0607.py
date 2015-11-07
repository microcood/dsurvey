# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 10, 25, 6, 7, 46, 549414, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='is_ongoing',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='group',
            name='comments',
            field=models.TextField(blank=True, verbose_name='Additional comments', null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.IntegerField(choices=[(2, 'Select multiple'), (1, 'Select one')], default=1),
        ),
        migrations.AlterField(
            model_name='test',
            name='comments',
            field=models.TextField(blank=True, verbose_name='Any additional comments', null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='file',
            field=models.FileField(upload_to='tests'),
        ),
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(max_length=400, verbose_name='Name of the test'),
        ),
    ]
