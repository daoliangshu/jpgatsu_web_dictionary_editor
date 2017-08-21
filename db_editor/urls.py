from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ajax_entries_request/$', views.ajax_entries_request),
    url(r'^ajax_update_request/$', views.ajax_update_request),
    url(r'^home$', views.home),
    url(r'^date$', views.getCurrentDate),
    url(r'^date/new/$', views.post_new, name='post_new'),
]
