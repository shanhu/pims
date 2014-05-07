# -*- coding: utf-8 -*- 
from django.views import generic

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
    #template_name = 'system/base_list.html'
    #todo add dynamic menus here!
    def get_context_data(self, **kwargs): 
        context = super(SystemListView, self).get_context_data(**kwargs)  
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

#--------------------------------------------------员工管理 界面定义------------------------------------------------------------------
from system.models import Employee, EmployeeForm
class EmployeeListView(SystemListView): 
    template_name = 'system/employee_list.html'
    context_object_name = 'employee_list'
    model = Employee
    def get_context_data(self, **kwargs): 
        context = super(EmployeeListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"员工汇总"
        context['title'] = u"员工汇总"
        return context
    
class EmployeeDetailView(SystemDetailView): 
    template_name = 'system/employee_detail.html'
    context_object_name = 'employee'
    model = Employee
    def get_context_data(self, **kwargs): 
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"员工详细信息"
        context['title'] = u"员工详细信息"
        return context 

from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

class EmployeeCreateView(CreateView):
    #form_class= EmployeeForm
    model = Employee
    def get_context_data(self, **kwargs):
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"员工注册"
        context['title'] = u"员工注册"
        return context
        
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
            
#--------------------------------------------------物料管理 界面定义------------------------------------------------------------------   
from system.models import MaterialType, MaterialTypeForm

class MaterialTypeListView(SystemListView): 
    template_name = 'system/materialType_list.html'
    context_object_name = 'materialType_list'
    model = MaterialType
    def get_context_data(self, **kwargs): 
        context = super(MaterialTypeListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"物料类型管理"
        context['title'] = u"物料类型管理"        
        return context  

class MaterialTypeDetailView(SystemDetailView): 
    template_name = 'system/materialType_detail.html'
    context_object_name = 'materialType'
    model = MaterialType
    def get_context_data(self, **kwargs): 
        context = super(MaterialTypeDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"详细物料类型详细信息"
        context['title'] = u"详细物料类型详细信息"
        return context
class MaterialTypeCreateView(CreateView):
    form_class= MaterialTypeForm
    model = MaterialType
    def get_context_data(self, **kwargs):
        context = super(MaterialTypeCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"详细物料类型详细信息"
        context['title'] = u"详细物料类型详细信息"
        return context
    success_url =  reverse_lazy("material_type_list")
        
class MaterialTypeUpdateView(UpdateView):
    form_class= MaterialTypeForm
    model = MaterialType
    
class MaterialTypeDeleteView(DeleteView):
    form_class= MaterialTypeForm
    model = MaterialType     
    success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        employee = self.get_object();
        if employee.cardNum1 != '' or employee.cardNum2 != '':
            employee.status = 0
            employee.save()
        else:
            employee.delete()
        return redirect('material_type_list');
