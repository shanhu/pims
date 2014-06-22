from django.conf.urls import patterns, url
 

from system import views

urlpatterns = patterns('',

    url(r'^$', views.IndexView.as_view(), name='index'),  
    url(r'^employee/$', views.EmployeeListView.as_view(), name='employee_list'), 
    url(r'^employees/(?P<pk>\d+)$', views.EmployeeDetailView.as_view(), name='employee_detail'), 
    url(r'^employee/add/$', views.EmployeeCreateView.as_view(), name='employee_add'), 
    url(r'^employee/(?P<pk>\d+)/$', views.EmployeeUpdateView.as_view(), name='employee_update'), 
    url(r'^employee/(?P<pk>\d+)/delete/$', views.EmployeeDeleteView.as_view(), name='employee_delete'), 
    
    
    
    url(r'^materialType/$', views.MaterialTypeListView.as_view(), name="material_type_list"),
    url(r'^materialType/add/$', views.MaterialTypeCreateView.as_view(), name="material_type_add"),
    url(r'^materialType/(?P<pk>\d+)/$', views.MaterialTypeUpdateView.as_view(), name="material_type_update"),
    url(r'^materialType/(?P<pk>\d+)/delete$', views.MaterialTypeDeleteView.as_view(), name="material_type_delete"),
    url(r'^materialTypes/(?P<pk>\d+)$', views.MaterialTypeDetailView.as_view(), name="material_type_detail"),
    

    url(r'^material/$', views.MaterialListView.as_view(), name="material_list"),
    url(r'^material/add/$', views.MaterialCreateView.as_view(), name="material_add"),
    url(r'^material/(?P<pk>\d+)/$', views.MaterialUpdateView.as_view(), name="material_update"),
    url(r'^material/(?P<pk>\d+)/delete$', views.MaterialDeleteView.as_view(), name="material_delete"),
    url(r'^materials/(?P<pk>\d+)$', views.MaterialDetailView.as_view(), name="material_detail"),
    
    
    
    url(r'^process/$', views.ProcessListView.as_view(), name="process_list"),
    url(r'^process/add/$', views.ProcessCreateView.as_view(), name="process_add"),
    url(r'^process/(?P<pk>\d+)/$', views.ProcessUpdateView.as_view(), name="process_update"),
    url(r'^process/(?P<pk>\d+)/delete$', views.ProcessDeleteView.as_view(), name="process_delete"),
    url(r'^processes/(?P<pk>\d+)$', views.ProcessDetailView.as_view(), name="process_detail"),
    
      
    url(r'^workclass/$', views.WorkClassListView.as_view(), name="workclass_list"),
    url(r'^workclass/add/$', views.WorkClassCreateView.as_view(), name="workclass_add"),
    url(r'^workclass/(?P<pk>\d+)/$', views.WorkClassUpdateView.as_view(), name="workclass_update"),
    url(r'^workclass/(?P<pk>\d+)/delete$', views.WorkClassDeleteView.as_view(), name="workclass_delete"),
    url(r'^workclasses/(?P<pk>\d+)$', views.WorkClassDetailView.as_view(), name="workclass_detail"),
    
    
    
    url(r'^salaryCount/$', views.SalaryCountConfigListView.as_view(), name="salarycount_list"),
    url(r'^salaryCount/add/$', views.SalaryCountConfigCreateView.as_view(), name="salarycount_add"),
    url(r'^salaryCount/(?P<pk>\d+)/$', views.SalaryCountConfigUpdateView.as_view(), name="salarycount_update"),
    url(r'^salaryCount/(?P<pk>\d+)/delete$', views.SalaryCountConfigDeleteView.as_view(), name="salarycount_delete"),
    url(r'^salaryCounts/(?P<pk>\d+)$', views.SalaryCountConfigDetailView.as_view(), name="salarycount_detail"),
    
    
    url(r'^salaryTime/$', views.SalaryTimeConfigListView.as_view(), name="salarytime_list"),
    url(r'^salaryTime/add/$', views.SalaryTimeConfigCreateView.as_view(), name="salarytime_add"),
    url(r'^salaryTime/(?P<pk>\d+)/$', views.SalaryTimeConfigUpdateView.as_view(), name="salarytime_update"),
    url(r'^salaryTime/(?P<pk>\d+)/delete$', views.SalaryTimeConfigDeleteView.as_view(), name="salarytime_delete"),
    url(r'^salaryTimes/(?P<pk>\d+)$', views.SalaryTimeConfigDetailView.as_view(), name="salarytime_detail"),
    
    
    
    url(r'^card/$', views.CardListView.as_view(), name="card_list"),
    url(r'^card/add/$', views.CardCreateView.as_view(), name="card_add"),
    url(r'^card/(?P<pk>\d+)/$', views.CardUpdateView.as_view(), name="card_update"),
    url(r'^card/(?P<pk>\d+)/delete$', views.CardDeleteView.as_view(), name="card_delete"),
    url(r'^cards/(?P<pk>\d+)$', views.CardDetailView.as_view(), name="card_detail"),
    
    url(r'^data/$', views.ProductionListView.as_view(), name="data_live"),
    url(r'^reportClass/$', views.ReportClassListView.as_view(), name="report_class"),
    url(r'^reportClassDetail/$', views.ReportClassDetailListView.as_view(), name="report_class_detail"),
    url(r'^reportEmployee/$', views.ReportEmployeeListView.as_view(), name="report_employee"),
    url(r'^reportEmployeeDetail/$', views.ReportEmployeeDetailListView.as_view(), name="report_employee_detail"),
    
    url(r'^terminal/$', views.TerminalListView.as_view(), name="terminal_list"),
    url(r'^workshop/$', views.WorkshopListView.as_view(), name="workshop_list"),
)
