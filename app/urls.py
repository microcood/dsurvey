from django.conf.urls import include, url
from django.contrib import admin
# from survey.views import WelcomeRedirectView


urlpatterns = [
    # url(r'^$', WelcomeRedirectView.as_view(), name="welcome"),
    url(r'^', include('survey.urls')),
    url(r'^manage/', include(admin.site.urls)),
    url(r'^fantasyland/visits/', include('tracking.urls')),
]
