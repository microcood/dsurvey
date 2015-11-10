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
# from survey.form import ResponseForm


class SurveyAccessMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.examination = Examination.get_ongoing()
        pk = kwargs.get('pk', None)
        if ((not self.examination or pk != str(self.examination.test.pk)) and not request.user.is_staff):
            messages.info(request, 'По данному адресу тестирований не проводится.')
            raise PermissionDenied
        elif not request.user.is_authenticated():
            request.session['next_page'] = request.path
            return redirect('examinee_register')
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
            return redirect('welcome')
        self.examination = Examination.get_ongoing()
        if not self.examination:
            messages.info(request, 'На данный момент тестирований не проводится.')
            raise PermissionDenied
        return super(ExamineeCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        existing_examinee = Examinee.objects.filter(
                group = self.examination.group,
                first_name = form.instance.first_name,
                middle_name = form.instance.middle_name,
                last_name = form.instance.last_name,
            ).last()

        if existing_examinee:
            print('hooray')
            user = existing_examinee.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, user)
            return redirect('welcome')

        import random
        user = User(
            username='@%s%s' % (unidecode(form.instance.first_name), random.randint(0,10000)),
            first_name = form.instance.first_name,
            last_name = form.instance.last_name,
            password='')
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        form.instance.user = user
        form.instance.group = self.examination.group
        form.save()
        return super(ExamineeCreateView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        next_page = self.request.session.get('next_page', None)
        self.request.session['next_page'] = None
        return next_page or reverse('welcome')


class TestCompletionView(SurveyAccessMixin, DetailView):
    model = Test
    template_name = 'test_completion.html'

    def dispatch(self, request, *args, **kwargs):
        self.examinee = Examinee.objects.filter(user__pk=request.user.pk).last()
        return super(TestCompletionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        test_response = TestResponse.objects.filter(
                examination=self.examination,
                examinee=self.examinee
            ).last()
        if test_response:
            messages.info(request, 'Вы уже прошли этот тест.')
            raise PermissionDenied
        return super(TestCompletionView, self).get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        test = self.get_object()
        test_response = TestResponse(test=test, examinee=self.examinee, examination=self.examination)
        test_response.save()
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


class ExaminationResultView(SurveyAccessMixin, ListView):
    model = TestResponse
    template_name = 'examination_result.html'

    def get_queryset(self, **kwargs):
        self.examination = Examination.objects.get(pk=self.kwargs['pk'])
        return self.model.objects.filter(examination=self.examination)


class TestResultView(SurveyAccessMixin, DetailView):
    model = Test
    template_name = 'test_result.html'

    def get_context_data(self, **kwargs):
        context = super(TestResultView, self).get_context_data(**kwargs)
        examinee_id = self.kwargs.get('examinee_id', None)
        if examinee_id:
            try:
                self.examinee = Examinee.objects.get(pk=examinee_id)
            except:
                messages.info(self.request, 'Результатов тестирования данного пользователя не найдено.')
                raise Http404
        else:
            try:
                self.examinee = self.request.user.examinee
            except:
                messages.info(self.request, 'Результатов вашего тестирования не найдено.')
                raise Http404

        test = self.get_object()
        test_response = TestResponse.objects.filter(test=test, examinee=self.examinee).last()
        total_count = test.questions.count()
        total_sum = 0
        context_questions = test.questions
        for question in context_questions:
            correct = question.answers.filter(is_correct=True)
            replies = test_response.replies.filter(question=question)
            correct_replies = replies.filter(answer__is_correct=True)
            question.correct_answers = []
            question.incorrect_answers = []

            # this part for template only
            for reply in replies:
                if reply.answer.is_correct:
                    question.correct_answers.append(reply.answer.pk)
                else:
                    question.incorrect_answers.append(reply.answer.pk)

            if correct.count() == replies.count() == correct_replies.count():
                total_sum += 1
                question.total = 1
            elif correct_replies.count() > 0:
                question.total = 0.5
                total_sum += 0.5
            else:
                question.total = 0

        results = (total_sum / total_count) * 100
        context['questions'] = context_questions
        context['test'] = test
        context['results'] = results
        context['test_response'] = test_response
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
