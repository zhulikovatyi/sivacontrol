from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = patterns('',
    url(r'^videos/$', views.VideoList.as_view()),
    url(r'^videos/(?P<pk>[0-9]+)$', views.VideoDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)