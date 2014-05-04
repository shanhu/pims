from django.conf.urls import patterns, url

from system import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),  
    url(r'^employee/$', views.EmployeeListView.as_view(), name='employee_list'), 
    url(r'^employee/(?P<pk>\d+)$', views.EmployeeDetailView.as_view(), name='employee_detail'), 
    url(r'employee/add/$', views.EmployeeCreate.as_view(), name='employee_add'),
    
)
