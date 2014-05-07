# -*- coding: utf-8 -*- 
from django.views import generic
from system.models import MaterialType, Material, Employee, EmployeeForm
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
 
    
class IndexView(generic.ListView):
    template_name = 'system/index.html'
    context_object_name = 'latest_materialType_list'
    def get_queryset(self):
        """Return the last five published polls."""
        return MaterialType.objects.order_by('id')[:5]

class SystemListView(generic.ListView):
    template_name = 'system/base_list.html'
    #todo add dynamic menus here!
    def get_context_data(self, **kwargs): 
        context = super(SystemListView, self).get_context_data(**kwargs) 
        context['menu_list'] = []
        context['breadcrumb'] = []
        context['pageHeader'] =  u"列表页"
        return context
        
class SystemDetailView(generic.DetailView):
    template_name = 'system/base_detail.html'
    #todo add dynamic menus here!
    def get_context_data(self, **kwargs): 
        context = super(SystemDetailView, self).get_context_data(**kwargs) 
        context['menu_list'] = []
        context['breadcrumb'] = []
        return context
        
class EmployeeListView(SystemListView): 
    template_name = 'system/employee_list.html'
    context_object_name = 'employee_list'
    model = Employee
    def get_context_data(self, **kwargs): 
        context = super(EmployeeListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"员工列表"
        return context
    
class EmployeeDetailView(SystemDetailView): 
    template_name = 'system/employee_detail.html'
    context_object_name = 'employee'
    model = Employee
    def get_context_data(self, **kwargs): 
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"员工详细信息"
        return context 

from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

class EmployeeCreateView(CreateView):
    form_class= EmployeeForm
    model = Employee
class EmployeeUpdateView(UpdateView):
    form_class= EmployeeForm
    model = Employee 
class EmployeeDeleteView(DeleteView):
    form_class= EmployeeForm
    model = Employee     
    success_url = reverse_lazy('employee_list')  
    def post(self,*args, **kwargs):
        employee = self.get_object();
        if employee.cardNum1 != '' or employee.cardNum2 != '':
            employee.status = 0
            employee.save()
        else:
            employee.delete()
        return redirect('employee_list');
            
   
   
    
