from django.conf.urls import patterns, include, url
from protracker import views

urlpatterns = patterns(
    '',
    url( r'^$', views.index, name='index' ),
    url( r'^alert_search/$', views.alert_search, name='alert_search' ),
    url( r'^(?P<alert_id>\d+)/alert_attr/$', views.alert_attr, name='alert_attr' ),
    url( r'^(?P<alert_id>\d+)/replicas/$', views.replicas, name='replicas' ),
    url( r'^derived_attr/(?P<attrname>\w+-\w+)/$', views.derived_attr, name='derived_attr' ),
    url( r'^derived_attr/rootcode/(?P<sha1>\w+)/$', views.attr_code, name='attr_code' ),
    url( r'^derived_attr/funccode/(?P<funcname>\w+)/(?P<sha1>\w+)/$', views.func_code, name='func_code' ),
    url( r'^(?P<replica_id>\d+)/replica_attr/$', views.replica_attr, name='replica_attr' ),
    url( r'^(?P<replica_id>\d+)/astro/$', views.astro, name='astro' ),
    url( r'^/locus/(?P<locus_id>\d+)/$', views.locus, name='locus' ),
    url( r'^/source/(?P<source_id>\d+)/$', views.source, name='source' ),
    url( r'^/image/(?P<image_id>\d+)/$', views.image, name='image' ),
)

