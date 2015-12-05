# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import survey.utils
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_testresponse_examination'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name_plural': 'Ответы', 'verbose_name': 'Ответ'},
        ),
        migrations.AlterModelOptions(
            name='examination',
            options={'verbose_name_plural': 'Тестирования', 'verbose_name': 'Тестирование'},
        ),
        migrations.AlterModelOptions(
            name='examinee',
            options={'verbose_name_plural': 'Проверяемые', 'verbose_name': 'Проверяемый'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name_plural': 'Группы', 'verbose_name': 'Группа'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name_plural': 'Вопросы', 'verbose_name': 'Вопрос'},
        ),
        migrations.AlterModelOptions(
            name='questionresponse',
            options={'verbose_name_plural': 'Результаты вопроса', 'verbose_name': 'Результат вопроса'},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'verbose_name_plural': 'Тесты', 'verbose_name': 'Тест'},
        ),
        migrations.AlterModelOptions(
            name='testresponse',
            options={'verbose_name_plural': 'Результаты теста', 'verbose_name': 'Результат теста'},
        ),
        migrations.AddField(
            model_name='examination',
            name='created',
            field=models.DateTimeField(verbose_name='Дата тестирования', auto_now_add=True, default=datetime.datetime(2015, 11, 7, 20, 26, 35, 713174, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=True, verbose_name='Является правильным'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(verbose_name='Вопрос', to='survey.Question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(verbose_name='Текст ответа'),
        ),
        migrations.AlterField(
            model_name='examination',
            name='group',
            field=models.ForeignKey(verbose_name='Группа', to='survey.Group'),
        ),
        migrations.AlterField(
            model_name='examination',
            name='is_ongoing',
            field=models.BooleanField(default=False, verbose_name='Продолжается в данный момент'),
        ),
        migrations.AlterField(
            model_name='examination',
            name='test',
            field=models.ForeignKey(verbose_name='Тест', to='survey.Test'),
        ),
        migrations.AlterField(
            model_name='examinee',
            name='first_name',
            field=models.CharField(verbose_name='Имя', max_length=100),
        ),
        migrations.AlterField(
            model_name='examinee',
            name='group',
            field=models.ForeignKey(verbose_name='Группа', to='survey.Group'),
        ),
        migrations.AlterField(
            model_name='examinee',
            name='last_name',
            field=models.CharField(verbose_name='Фамилия', max_length=100),
        ),
        migrations.AlterField(
            model_name='examinee',
            name='middle_name',
            field=models.CharField(verbose_name='Отчество', max_length=100),
        ),
        migrations.AlterField(
            model_name='examinee',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='group',
            name='comments',
            field=models.TextField(blank=True, verbose_name='Дополнительный комментарий', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='created',
            field=models.DateTimeField(verbose_name='Дата создания', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(verbose_name='Название', max_length=400),
        ),
        migrations.AlterField(
            model_name='question',
            name='position',
            field=models.IntegerField(default=0, verbose_name='Позиция'),
        ),
        migrations.AlterField(
            model_name='question',
            name='test',
            field=models.ForeignKey(verbose_name='Тест', to='survey.Test'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(verbose_name='Текст вопроса'),
        ),
        migrations.AlterField(
            model_name='questionresponse',
            name='answer',
            field=models.ForeignKey(verbose_name='Ответ', to='survey.Answer'),
        ),
        migrations.AlterField(
            model_name='questionresponse',
            name='question',
            field=models.ForeignKey(verbose_name='Вопрос', to='survey.Question'),
        ),
        migrations.AlterField(
            model_name='questionresponse',
            name='test_response',
            field=models.ForeignKey(verbose_name='Результат теста', to='survey.TestResponse'),
        ),
        migrations.AlterField(
            model_name='test',
            name='comments',
            field=models.TextField(blank=True, verbose_name='Дополнительный комментарий', null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='created',
            field=models.DateTimeField(verbose_name='Дата создания', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='file',
            field=models.FileField(verbose_name='Файл', upload_to=survey.utils.generate_filename),
        ),
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(verbose_name='Название', max_length=400),
        ),
        migrations.AlterField(
            model_name='test',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='testresponse',
            name='created',
            field=models.DateTimeField(verbose_name='Дата создания', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='testresponse',
            name='examination',
            field=models.ForeignKey(verbose_name='Тестирование', to='survey.Examination'),
        ),
        migrations.AlterField(
            model_name='testresponse',
            name='examinee',
            field=models.ForeignKey(verbose_name='Проеверяемый', to='survey.Examinee'),
        ),
        migrations.AlterField(
            model_name='testresponse',
            name='test',
            field=models.ForeignKey(verbose_name='Тест', to='survey.Test'),
        ),
    ]
