from django.conf.urls import include
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ajax_entries_request/$', views.ajax_entries_request),
    url(r'^ajax_update_request/$', views.ajax_update_request),
    url(r'^ajax_remove_request/$', views.ajax_remove_request),
    url(r'^home$', views.home_view),
    url(r'^date/new/$', views.post_new, name='post_new'),
    url(r'^download_csv/$', views.get_dictionary_as_csv),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', views.logout_view),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/', include('django.contrib.auth.urls')),

]
