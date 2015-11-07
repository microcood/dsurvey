# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_auto_20151025_0607'),
    ]

    operations = [
        migrations.CreateModel(
            name='Examination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('is_ongoing', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='group',
            name='is_ongoing',
        ),
        migrations.RemoveField(
            model_name='question',
            name='type',
        ),
        migrations.AddField(
            model_name='examination',
            name='group',
            field=models.ForeignKey(to='survey.Group'),
        ),
        migrations.AddField(
            model_name='examination',
            name='test',
            field=models.ForeignKey(to='survey.Test'),
        ),
    ]
