from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import *


class AnswerInline(admin.StackedInline):
    model = Answer


class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [
        AnswerInline
    ]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline
    ]


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'test', 'is_ongoing']
    readonly_fields = ('examination_results', )

    def examination_results(self, instance):
        if instance.pk:
            link =  reverse('examination_result',kwargs={ 'pk': instance.pk})
            return mark_safe('<a href="%s">Результаты</a>' % link)
        return 'Результатов тестирования на данный момент нет'


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
