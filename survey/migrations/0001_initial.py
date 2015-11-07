# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('is_correct', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Examinee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comments', models.TextField(null=True, verbose_name=b'Additional comments', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('position', models.IntegerField(default=0)),
                ('type', models.IntegerField(default=1, choices=[(2, b'Select multiple'), (1, b'Select one')])),
            ],
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.ForeignKey(to='survey.Answer')),
                ('question', models.ForeignKey(to='survey.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=400, verbose_name=b'Name of the test')),
                ('comments', models.TextField(null=True, verbose_name=b'Any additional comments', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=b'tests')),
            ],
        ),
        migrations.CreateModel(
            name='TestResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('examinee', models.ForeignKey(to='survey.Examinee')),
                ('test', models.ForeignKey(to='survey.Test')),
            ],
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='test_response',
            field=models.ForeignKey(to='survey.TestResponse'),
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(to='survey.Test'),
        ),
        migrations.AddField(
            model_name='examinee',
            name='group',
            field=models.ForeignKey(to='survey.Group'),
        ),
        migrations.AddField(
            model_name='examinee',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='survey.Question'),
        ),
    ]
