from django.conf.urls import patterns, include, url
from protracker import views

urlpatterns = patterns(
    '',
    url( r'^$', views.index, name='index' ),
    url( r'^alert_search/$', views.alert_search, name='alert_search' ),
    url( r'^(?P<alert_id>\d+)/alert_attr/$', views.alert_attr, name='alert_attr' ),
    url( r'^derived_attr/(?P<attrname>\w+-\w+)/$', views.derived_attr, name='derived_attr' ),
)
