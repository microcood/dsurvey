from django.db import models
from django.utils.functional import cached_property
from django.contrib.auth.models import User
from .utils import generate_filename


class Group(models.Model):
    name = models.CharField(verbose_name = 'Название', max_length=400)
    created = models.DateTimeField(verbose_name = 'Дата создания', auto_now_add=True)
    comments = models.TextField(
        verbose_name = 'Дополнительный комментарий', blank=True, null=True)

    @property
    def examinees(self):
        return Examinee.objects.filter(group=self.pk)

    def __str__(self):
        return (self.name)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Examinee(models.Model):
    last_name = models.CharField(verbose_name = 'Фамилия', max_length=100)
    first_name = models.CharField(verbose_name = 'Имя', max_length=100)
    middle_name = models.CharField(verbose_name = 'Отчество', max_length=100)

    user = models.OneToOneField(User, verbose_name = 'Пользователь')
    group = models.ForeignKey(Group, verbose_name = 'Группа')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Проверяемый'
        verbose_name_plural = 'Проверяемые'


class Test(models.Model):
    name = models.CharField(verbose_name = 'Название', max_length=400)
    comments = models.TextField(
        verbose_name = 'Дополнительный комментарий', blank=True, null=True)
    created = models.DateTimeField(verbose_name = 'Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name = 'Дата обновления', auto_now=True)
    file = models.FileField(verbose_name = 'Файл', upload_to=generate_filename)

    @property
    def questions(self):
        return Question.objects.filter(test=self.pk)

    def __str__(self):
        return (self.name)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Examination(models.Model):
    group = models.ForeignKey(Group, verbose_name = 'Группа')
    test = models.ForeignKey(Test, verbose_name = 'Тест')
    is_ongoing = models.BooleanField(verbose_name = 'Продолжается в данный момент', default=False)

    @classmethod
    def get_ongoing(self):
        try:
            return self.objects.get(is_ongoing=True)
        except self.DoesNotExist:
            return None

    def save(self):
        if self.is_ongoing:
            current = self.get_ongoing()
            if current and current != self:
                current.is_ongoing = False
                current.save()
        super(Examination, self).save()

    class Meta:
        verbose_name = 'Тестирорвание'
        verbose_name_plural = 'Тестирования'


class Question(models.Model):
    test = models.ForeignKey(Test, verbose_name = 'Тест')
    text = models.TextField(verbose_name = 'Текст вопроса')
    position = models.IntegerField(verbose_name = 'Позиция', default=0)

    @property
    def answers(self):
        return Answer.objects.filter(question=self.pk)

    def __str__(self):
        return (self.text)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name = 'Вопрос')
    text = models.TextField(verbose_name = 'Текст ответа')
    is_correct = models.BooleanField(verbose_name = 'Является правильным', default=True)

    def __str__(self):
        return (self.text)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class TestResponse(models.Model):
    examination = models.ForeignKey(Examination, verbose_name = 'Тестирование')
    test = models.ForeignKey(Test, verbose_name = 'Тест')
    examinee = models.ForeignKey(Examinee, verbose_name = 'Проеверяемый')
    created = models.DateTimeField(verbose_name = 'Дата создания', auto_now_add=True)

    @property
    def replies(self):
        return QuestionResponse.objects.filter(test_response=self.pk)

    @cached_property
    def result_percent(self):
        questions = self.test.questions
        total_sum = 0
        for question in questions:
            correct = question.answers.filter(is_correct=True)
            replies = self.replies.filter(question=question)
            correct_replies = replies.filter(answer__is_correct=True)

            if correct.count() == replies.count() == correct_replies.count():
                total_sum += 1
            elif correct_replies.count() > 0:
                total_sum += 0.5

        return (total_sum / questions.count()) * 100

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты теста'


class QuestionResponse(models.Model):
    test_response = models.ForeignKey(TestResponse, verbose_name = 'Результат теста')
    question = models.ForeignKey(Question, verbose_name = 'Вопрос')
    answer = models.ForeignKey(Answer, verbose_name = 'Ответ')

    class Meta:
        verbose_name = 'Результат вопроса'
        verbose_name_plural = 'Результаты вопроса'
