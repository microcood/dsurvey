from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import *


class AnswerInline(admin.StackedInline):
    model = Answer


class QuestionInline(admin.StackedInline):
    model = Question
    list_filter = ('test', )
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
    inlines = [
        AnswerInline
    ]

@admin.register(Examinee)
class ExamineeAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name', 'first_name', 'middle_name']



# @admin.register(TestResponse)
# class TestResponseAdmin(admin.ModelAdmin):
#     pass


# @admin.register(QuestionResponse)
# class QuestionResponseAdmin(admin.ModelAdmin):
#     pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
     list_display = ['id', 'text', 'is_correct']
