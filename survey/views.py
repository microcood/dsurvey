# -*- coding:utf-8 -*-
from unidecode import unidecode
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import FormView, RedirectView, DetailView, ListView
from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied
from django.forms.models import modelform_factory
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import *


class IndexView(ListView):
    model = Group

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home')
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        from django import forms

        class GroupForm(forms.Form):
            group_code = forms.IntegerField(required=True, label='')
        context['form'] = GroupForm()
        return context

    def post(self, request, *args, **kwargs):
        group_code = request.POST.get('group_code')
        qs = self.model.objects.distinct().filter(examination__is_ongoing=True).values_list('code', flat=True)
        if group_code not in qs:
            messages.info(self.request, 'Номер введен не верно.')
            return redirect('home')
        return redirect('group', group_code=group_code)


class GroupView(DetailView):
    model = Group

    def dispatch(self, request, *args, **kwargs):
        self.code = kwargs.get('group_code')
        self.examinations = Examination.objects.filter(is_ongoing=True,
                                                       group__code=self.code)
        if not self.examinations.exists() and not request.user.is_staff:
            raise PermissionDenied
        if request.user.is_authenticated():
            return redirect('home')
        return super(GroupView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Group, code=self.code)

    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)
        context['create_form'] = modelform_factory(Examinee,
                                                   exclude=('group', 'user'))
        from django import forms

        examinees = self.object.examinee_set.all().order_by('last_name')
        form_choices = [(a.user.id, a) for a in examinees]

        class UsersForm(forms.Form):
            user = forms.ChoiceField(choices=form_choices,
                                     label="Пользователь",
                                     required=True)
        context['select_form'] = UsersForm()
        return context

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user')
        user = get_object_or_404(User, id=user_id)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return redirect('home')


class ExamineeView(DetailView):
    model = Examinee

    def dispatch(self, request, *args, **kwargs):
        self.examinee_id = self.kwargs.get('examinee_id', None)
        if request.user.is_staff:
            if not self.examinee_id:
                return redirect('admin:index')
            else:
                self.object = get_object_or_404(Examinee, id=self.examinee_id)
        else:
            if not hasattr(request.user, 'examinee'):
                return redirect('index')
            self.object = request.user.examinee
        return super(ExamineeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ExamineeView, self).get_context_data(**kwargs)
        context['done_tests'] = \
            TestResponse.objects.filter(examinee_id=self.object.id)
        context['tests_todo'] = Test.objects.filter(examination__is_ongoing=True, examination__group=self.object.group)
        return context

    def get_object(self):
        return self.object


class SurveyAccessMixin(object):

    def dispatch(self, request, *args, **kwargs):
        return super(SurveyAccessMixin, self).dispatch(request, *args, **kwargs)


class WelcomeRedirectView(RedirectView):
    permanent = False
    pattern_name = 'test_completion'

    def get_redirect_url(self, *args, **kwargs):
        self.examination = Examination.get_ongoing()
        if not self.examination:
            messages.info(self.request, 'На данный момент тестирований не проводится.')
            raise PermissionDenied
        kwargs['pk'] = self.examination.test.pk
        return super(WelcomeRedirectView, self).get_redirect_url(*args, **kwargs)


class ExamineeCreateView(FormView):
    template_name = 'examinee_register.html'
    form_class = modelform_factory(Examinee, exclude=('group', 'user'))

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('index')
        return super(ExamineeCreateView, self).dispatch(request,
                                                        *args, **kwargs)

    def form_valid(self, form):
        group = get_object_or_404(Group, code=self.kwargs.get('group_code'))
        existing_examinee = Examinee.objects.distinct().filter(
                group=group,
                first_name__icontains=form.instance.first_name,
                middle_name__icontains=form.instance.middle_name,
                last_name__icontains=form.instance.last_name,
            ).last()

        if existing_examinee:
            user = existing_examinee.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, user)
            return redirect('home')

        import random
        user = User(
            username='@%s%s' % (unidecode(form.instance.first_name),
                                random.randint(0, 1000)),
            first_name=form.instance.first_name,
            last_name=form.instance.last_name,
            password='')
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        form.instance.user = user
        form.instance.group = group
        form.save()
        return super(ExamineeCreateView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('home')


class TestCompletionView(SurveyAccessMixin, DetailView):
    model = Test
    template_name = 'test_completion.html'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'examinee'):
            return redirect('home')
        self.object = get_object_or_404(Test, pk=self.kwargs.get('pk'))
        self.examinee = request.user.examinee
        self.examination = Examination.objects.filter(test=self.object,group=self.examinee.group, is_ongoing=True).last()
        if not self.examination:
            return redirect('home')
        return super(TestCompletionView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TestCompletionView, self).get_context_data(**kwargs)
        presaved_results = TestResponsePresave.objects.filter(
                                               test=self.object,
                                               examinee=self.examinee,
                                               examination=self.examination).last()
        if presaved_results:
            context['seconds_left'] = presaved_results.seconds_left
            context['checked_questions'] = QuestionResponse.objects.filter(test_response=presaved_results).values_list('answer_id', flat=True)
        else:
            context['seconds_left'] = self.object.time
        return context

    def post(self, request, *args, **kwargs):
        test = self.get_object()
        test_response = TestResponse(test=test, examinee=self.examinee, examination=self.examination)
        test_response.save()
        presaved_results = TestResponsePresave.objects.filter(
                                               test=self.object,
                                               examinee=self.examinee,
                                               examination=self.examination).delete()
        for question in test.questions:
            q_response = request.POST.getlist(str(question.id), None)
            if q_response:
                for answer in question.answers:
                    if str(answer.id) in q_response:
                        question_response = QuestionResponse(
                            test_response=test_response,
                            question=question,
                            answer=answer)
                        question_response.save()
        return redirect('test_result', pk=test.pk)


class TestInternResultsView(DetailView):
    model = Test

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'examinee'):
            return redirect('home')
        self.object = get_object_or_404(Test, pk=self.kwargs.get('pk'))
        self.examinee = request.user.examinee
        self.examination = Examination.objects.filter(test=self.object,group=self.examinee.group, is_ongoing=True).last()
        if not self.examination:
            raise Http404()
        return super(TestInternResultsView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        test = self.get_object()
        test_response, created = TestResponsePresave.objects.get_or_create(
                                            test=test,
                                            examinee=self.examinee,
                                            examination=self.examination)

        test_response.seconds_left = request.POST.get("seconds_left", 0)
        test_response.save()
        if not created:
            QuestionResponse.objects.filter(test_response=test_response).delete()
        for question in test.questions:
            q_response = request.POST.getlist(str(question.id), None)
            if q_response:
                for answer in question.answers:
                    if str(answer.id) in q_response:
                        question_response = QuestionResponse(
                            test_response=test_response,
                            question=question,
                            answer=answer)
                        question_response.save()
        return HttpResponse()
        # return super(TestInternResultsView, self).get(request, *args, **kwargs)


class ExaminationResultView(ListView):
    model = TestResponse
    template_name = 'examination_result.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(ExaminationResultView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        self.examination = Examination.objects.get(pk=self.kwargs['pk'])
        return self.model.objects.filter(examination=self.examination)


class MostFailedQuestionsView(ListView):
    model = Question
    template_name = 'examination_failed.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        self.examination = Examination.objects.get(pk=self.kwargs['pk'])
        return super(MostFailedQuestionsView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        self.level = int(self.request.GET.get('level', 5))
        test_responses = TestResponse.objects.filter(examination=self.examination)
        bad_questions = {}
        for test_response in test_responses:
            for question in self.examination.test.questions:
                if not bad_questions.get(question.pk, None):
                    bad_questions[question.pk] = 0
                correct = question.answers.filter(is_correct=True)
                replies = test_response.replies.filter(question=question)
                correct_replies = replies.filter(answer__is_correct=True)

                if correct.count() == replies.count() == correct_replies.count():
                    pass
                else:
                    bad_questions[question.pk] += 1
        bad_list = [key for key, value in bad_questions.items() if value > self.level]

        qs = self.model.objects.filter(test=self.examination.test)
        qs = qs.filter(pk__in=bad_list)
        return qs


class TestResultView(SurveyAccessMixin, DetailView):
    model = Test
    template_name = 'test_result.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.examinee = Examinee.objects.filter(pk=kwargs.get('examinee_id')).last()
        elif request.user.is_authenticated():
            self.examinee = request.user.examinee
        else:
            return redirect('home')
        self.test_response = TestResponse.objects.filter(test=self.get_object(), examinee=self.examinee).last()
        if not self.test_response:
            return redirect('home')
        return super(TestResultView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TestResultView, self).get_context_data(**kwargs)
        total_count = self.object.questions.count()
        total_sum = 0
        context_questions = self.object.questions
        incorrect_questions = context_questions.filter(
                        answer__is_correct=False).values_list('id', flat=True)
        results = self.test_response.result_percent
        context['questions'] = context_questions
        context['incorrect_questions'] = incorrect_questions
        context['test'] = self.object
        context['results'] = results
        context['test_response'] = self.test_response
        return context


@staff_member_required
def examination_excel(request, pk):
    import xlsxwriter
    import io
    import datetime

    examination = get_object_or_404(Examination, pk=pk)
    test_responses = TestResponse.objects.filter(examination=examination)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=examination_%s.xlsx' % examination.pk

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format()
    header_format.set_bold()
    header_format.set_bg_color('silver')
    worksheet.set_row(0, 30)
    worksheet.set_column('A:A', 50)
    worksheet.write(0, 0, 'ФИО', header_format)
    worksheet.write(0, 1, 'Балл', header_format)
    worksheet.write(0, 2, 'Дата', header_format)

    row = 1
    for obj in test_responses:
        cformat = workbook.add_format()
        if obj.result_percent > 70:
            cformat.set_bg_color('green')
        worksheet.set_row(row, 30)
        worksheet.write(row, 0, str(obj.examinee))
        worksheet.write(row, 1, '%s%s' % (obj.result_percent, '%'), cformat)
        worksheet.write(row, 2, examination.created.strftime('%d.%m.%Y'))
        row += 1

    workbook.close()

    output.seek(0)
    response.write(output.read())
    return response
