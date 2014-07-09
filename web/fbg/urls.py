from django.conf.urls import patterns, include, url

urlpatterns = patterns('fbg.views',
    url(r'^$', 'index'),
    url(r'^env/(?P<nrs_environment_id>\d+)/$', 'env_detail'),
    url(r'^node/(?P<nrs_node_id>\d+)/$', 'node_detail'),
    url(r'^(?P<nrs_environment_id>\d+)/results/$', 'results'),
    url(r'^(?P<nrs_environment_id>\d+)/update/$', 'update'),
)
