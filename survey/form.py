# from django import forms
# from django.forms import models
# from .models import Question, TestResponse
#
#
# class ResponseForm(models.ModelForm):
#
#     class Meta:
#         model = TestResponse
#         fields = ['test']
#
#     def __init__(self, questions=None, *args, **kwargs):
#         super(ResponseForm, self).__init__(*args, **kwargs)
#
#         for q in questions:
#             if q.type == Question.SELECT_MULTIPLE:
#                 self.fields["question_%d" % q.pk] = forms.MultipleChoiceField(
#                     label=q.text, choices=q.answers)
#             else:
#                 self.fields["question_%d" % q.pk] = forms.ChoiceField(
#                     label=q.text, choices=q.answers)
#
#
#     # def save(self, commit=True):
#     #     response = super(ResponseForm, self).save(commit=False)
