# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import *


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionInline(admin.StackedInline):
    model = Question
    inlines = [
        AnswerInline
    ]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'test', 'created', 'is_ongoing']
    readonly_fields = ('examination_results', 'export_xls', 'most_failed')

    def examination_results(self, instance):
        if instance.pk:
            link = reverse('examination_result',kwargs={ 'pk': instance.pk})
            return mark_safe('<a href="%s">Результаты</a>' % link)
        return 'Результатов тестирования на данный момент нет'

    def export_xls(self, instance):
        if instance.pk:
            link = reverse('examination_excel',kwargs={ 'pk': instance.pk})
            return mark_safe('<a href="%s">Результаты в excel</a>' % link)
        return 'Результатов тестирования в excel тоже пока нет'

    def most_failed(self, instance):
        if instance.pk:
            link = reverse('examination_failed',kwargs={ 'pk': instance.pk})
            return mark_safe('<a href="%s">Самые трудные вопросы</a>' % link)
        return 'Тут тоже пусто'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created', 'examinees_count']

    def examinees_count(self, instance):
        return instance.examinees.count()


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    list_filter = ('test', )
    inlines = [
        AnswerInline
    ]


@admin.register(Examinee)
class ExamineeAdmin(admin.ModelAdmin):
    actions = ('merge', )
    list_display = ['id', 'last_name', 'first_name', 'middle_name', 'group', 'exams']
    readonly_fields = ('results', )
    list_filter = ('group', )

    def results(self, instance):
        results = instance.testresponse_set.all().order_by("test__name")
        if results:
            result_string = '<table>'
            for result in results:
                result_string += '<tr><td>%s</td><td>%s&#37;</td></tr>' % \
                                        (result.test, result.result_percent)
            return result_string + '</table>'
        return 'Нет результатов'

    results.allow_tags = True
    results.short_description = "Результаты"

    def exams(self, instance):
        return instance.testresponse_set.count()

    exams.short_description = "Пройдено тестов"

    def merge(self, request, queryset):
        main = queryset[0]
        tail = queryset[1:]
        for dub in tail:
            main.testresponse_set.add(*dub.testresponse_set.all())
            dub.delete()

    merge.short_description = "Объединить тесты"

# @admin.register(TestResponse)
# class TestResponseAdmin(admin.ModelAdmin):
#     pass


# @admin.register(QuestionResponse)
# class QuestionResponseAdmin(admin.ModelAdmin):
#     pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
     list_display = ['id', 'text', 'is_correct']
     search_fields = ['text']
