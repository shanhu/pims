from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from system import views

urlpatterns = patterns('',

    url(r'^$', views.IndexView.as_view(), name='index'),      
    url(r'^employee/$', login_required(views.EmployeeListView.as_view()), name='employee_list'), 
    url(r'^employees/(?P<pk>\d+)$', login_required(views.EmployeeDetailView.as_view()), name='employee_detail'), 
    url(r'^employee/add/$', login_required(views.EmployeeCreateView.as_view()), name='employee_add'), 
    url(r'^employee/(?P<pk>\d+)/$', login_required(views.EmployeeUpdateView.as_view()), name='employee_update'), 
    url(r'^employee/(?P<pk>\d+)/delete/$', login_required(views.EmployeeDeleteView.as_view()), name='employee_delete'), 
    
    
    
    url(r'^materialType/$', login_required(views.MaterialTypeListView.as_view()), name="material_type_list"),
    url(r'^materialType/add/$', login_required(views.MaterialTypeCreateView.as_view()), name="material_type_add"),
    url(r'^materialType/(?P<pk>\d+)/$', login_required(views.MaterialTypeUpdateView.as_view()), name="material_type_update"),
    url(r'^materialType/(?P<pk>\d+)/delete$', login_required(views.MaterialTypeDeleteView.as_view()), name="material_type_delete"),
    url(r'^materialTypes/(?P<pk>\d+)$', login_required(views.MaterialTypeDetailView.as_view()), name="material_type_detail"),
    

    url(r'^material/$', login_required(views.MaterialListView.as_view()), name="material_list"),
    url(r'^material/add/$', login_required(views.MaterialCreateView.as_view()), name="material_add"),
    url(r'^material/(?P<pk>\d+)/$', login_required(views.MaterialUpdateView.as_view()), name="material_update"),
    url(r'^material/(?P<pk>\d+)/delete$', login_required(views.MaterialDeleteView.as_view()), name="material_delete"),
    url(r'^materials/(?P<pk>\d+)$', login_required(views.MaterialDetailView.as_view()), name="material_detail"),
    
    
    
    url(r'^process/$', login_required(views.ProcessListView.as_view()), name="process_list"),
    url(r'^process/add/$', login_required(views.ProcessCreateView.as_view()), name="process_add"),
    url(r'^process/(?P<pk>\d+)/$', login_required(views.ProcessUpdateView.as_view()), name="process_update"),
    url(r'^process/(?P<pk>\d+)/delete$', login_required(views.ProcessDeleteView.as_view()), name="process_delete"),
    url(r'^processes/(?P<pk>\d+)$', login_required(views.ProcessDetailView.as_view()), name="process_detail"),
    
      
    url(r'^workclass/$', login_required(views.WorkClassListView.as_view()), name="workclass_list"),
    url(r'^workclass/add/$', login_required(views.WorkClassCreateView.as_view()), name="workclass_add"),
    url(r'^workclass/(?P<pk>\d+)/$', login_required(views.WorkClassUpdateView.as_view()), name="workclass_update"),
    url(r'^workclass/(?P<pk>\d+)/delete$', login_required(views.WorkClassDeleteView.as_view()), name="workclass_delete"),
    url(r'^workclasses/(?P<pk>\d+)$', login_required(views.WorkClassDetailView.as_view()), name="workclass_detail"),
    
    
    
    url(r'^salaryCount/$', login_required(views.SalaryCountConfigListView.as_view()), name="salarycount_list"),
    url(r'^salaryCount/add/$', login_required(views.SalaryCountConfigCreateView.as_view()), name="salarycount_add"),
    url(r'^salaryCount/(?P<pk>\d+)/$', login_required(views.SalaryCountConfigUpdateView.as_view()), name="salarycount_update"),
    url(r'^salaryCount/(?P<pk>\d+)/delete$',login_required( views.SalaryCountConfigDeleteView.as_view()), name="salarycount_delete"),
    url(r'^salaryCounts/(?P<pk>\d+)$', login_required(views.SalaryCountConfigDetailView.as_view()), name="salarycount_detail"),
    
    
    
    url(r'^salaryTime/$', login_required(views.SalaryTimeConfigListView.as_view()), name="salarytime_list"),
    url(r'^salaryTime/add/$', login_required(views.SalaryTimeConfigCreateView.as_view()), name="salarytime_add"),
    url(r'^salaryTime/(?P<pk>\d+)/$',login_required( views.SalaryTimeConfigUpdateView.as_view()), name="salarytime_update"),
    url(r'^salaryTime/(?P<pk>\d+)/delete$',login_required(views.SalaryTimeConfigDeleteView.as_view()), name="salarytime_delete"),
    url(r'^salaryTimes/(?P<pk>\d+)$', login_required(views.SalaryTimeConfigDetailView.as_view()), name="salarytime_detail"),
    
    
    
    url(r'^card/$',login_required( views.CardListView.as_view()), name="card_list"),
    url(r'^card/add/$',login_required( views.CardCreateView.as_view()), name="card_add"),
    url(r'^card/(?P<pk>\d+)/$',login_required( views.CardUpdateView.as_view()), name="card_update"),
    url(r'^card/(?P<pk>\d+)/delete$',login_required( views.CardDeleteView.as_view()), name="card_delete"),
    url(r'^cards/(?P<pk>\d+)$', login_required(views.CardDetailView.as_view()), name="card_detail"),
    
    url(r'^data/$', login_required(views.ProductionListView.as_view()), name="data_live"),
    url(r'^report/generate/$', 'system.views.generate_realTimeReport'), 
    url(r'^reportClass/$',login_required( views.ReportClassListView.as_view()), name="report_class"),
    url(r'^reportClass/export/Class$', 'system.views.export_reportClass'),
    url(r'^reportClass/export/ClassDetail$', 'system.views.export_reportClassDetail'),
    url(r'^reportClassReal/$',login_required( views.ReportClassRealTimeListView.as_view()), name="real_report_class"),
    url(r'^reportClassDetail/$',login_required( views.ReportClassDetailListView.as_view()), name="report_class_detail"),
    url(r'^reportEmployee/$', login_required(views.ReportEmployeeListView.as_view()), name="report_employee"),
    url(r'^reportEmployee/export/Employee$', 'system.views.export_reportEmployee'),
    url(r'^reportEmployeeReal/$', login_required(views.ReportEmployeeRealTimeListView.as_view()), name="real_report_employee"),
    url(r'^reportEmployeeDetail/$',login_required( views.ReportEmployeeDetailListView.as_view()), name="report_employee_detail"),
    url(r'^reportEmployee/export/EmployeeDetail$', 'system.views.export_reportEmployeedetail'),
    url(r'^reportSalary/$',login_required( views.SalaryReportListView.as_view()), name="report_salary_list"),
    url(r'^reportSalary/export/$', 'system.views.export_salaryReport'), 
    
    url(r'^terminal/$',login_required( views.TerminalListView.as_view()), name="terminal_list"),
    url(r'^workshop/$',login_required( views.WorkshopListView.as_view()), name="workshop_list"),
    
    
   
    
    
    
    
    
)
