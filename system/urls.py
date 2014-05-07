from django.conf.urls import patterns, url
from system.models import EmployeeForm
from system.formpreview import EmployeeFormPreview
from system import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),  
    url(r'^employee/$', views.EmployeeListView.as_view(), name='employee_list'), 
    url(r'^employees/(?P<pk>\d+)$', views.EmployeeDetailView.as_view(), name='employee_detail'), 
    url(r'^employee/add/$', views.EmployeeCreateView.as_view(), name='employee_add'), 
    url(r'^employee/(?P<pk>\d+)/$', views.EmployeeUpdateView.as_view(), name='employee_update'), 
    url(r'^employee/(?P<pk>\d+)/delete/$', views.EmployeeDeleteView.as_view(), name='employee_delete'), 
    
    url(r'^employee/form/employeeFormPreview$', EmployeeFormPreview(EmployeeForm)),
    

    
)
