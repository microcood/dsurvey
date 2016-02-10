from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<group_code>[0-9]+)/$', GroupView.as_view(), name='group'),
    url(r'^home/(?P<examinee_id>[0-9]+)/$',
        ExamineeView.as_view(),
        name='home'),
    url(r'^(?P<group_code>[0-9]+)/register/$',
        ExamineeCreateView.as_view(),
        name="examinee_register"),
    url(r'^home/$', ExamineeView.as_view(), name='home'),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name="logout"),
    url(r'^examination/(?P<pk>\d+)/result/$',
        ExaminationResultView.as_view(),
        name="examination_result"),
    url(r'^examination/(?P<pk>\d+)/excel/$',
        examination_excel,
        name="examination_excel"),
    url(r'^examination/(?P<pk>\d+)/failed/$',
        MostFailedQuestionsView.as_view(),
        name="examination_failed"),
    url(r'^test/(?P<pk>\d+)/results/(?P<examinee_id>\d+)/$',
        TestResultView.as_view(),
        name="test_result"),
    url(r'^test/(?P<pk>\d+)/results/$',
        TestResultView.as_view(),
        name="test_result"),
    url(r'^test/(?P<pk>\d+)/$',
        TestCompletionView.as_view(),
        name="test_completion")
]
