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
    
    
    url(r'^materialType/$', views.MaterialTypeListView.as_view(), name="material_type_list"),
    url(r'^materialType/add/$', views.MaterialTypeCreateView.as_view(), name="material_type_add"),
    url(r'^materialType/add/$', views.MaterialTypeUpdateView.as_view(), name="material_type_update"),
    url(r'^materialType/add/$', views.MaterialTypeDeleteView.as_view(), name="material_type_delete"),
    url(r'^materialTypes/(?P<pk>\d+)$', views.MaterialTypeDetailView.as_view(), name="material_type_detail"),
    

    
)
