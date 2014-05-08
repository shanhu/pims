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
    paginate_by = 10
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
    form_class= EmployeeForm
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
            
#--------------------------------------------------物料类型管理 界面定义------------------------------------------------------------------   
from system.models import MaterialType, MaterialTypeForm

class MaterialTypeListView(SystemListView): 
    template_name = 'system/materialType_list.html'
    context_object_name = 'materialType_list'
    model = MaterialType
    paginate_by = 10
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
        context['pageHeader'] = u"物料类型详细信息"
        context['title'] = u"物料类型详细信息"
        return context
class MaterialTypeCreateView(CreateView):
    form_class= MaterialTypeForm
    model = MaterialType
    def get_context_data(self, **kwargs):
        context = super(MaterialTypeCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"物料类型详细信息"
        context['title'] = u"物料类型详细信息"
        return context
    success_url =  reverse_lazy("material_type_list")
        
class MaterialTypeUpdateView(UpdateView):
    form_class= MaterialTypeForm
    model = MaterialType
    success_url =  reverse_lazy("material_type_list")
    
class MaterialTypeDeleteView(DeleteView):
    form_class= MaterialTypeForm
    model = MaterialType     
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        materialType = self.get_object(); 
        materialType.status = 0
        materialType.save() 
        return redirect('material_type_list');
           
#--------------------------------------------------物料管理 界面定义------------------------------------------------------------------   
from system.models import Material, MaterialForm

class MaterialListView(SystemListView): 
    template_name = 'system/material_list.html'
    context_object_name = 'material_list'
    model = Material
    paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(MaterialListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"物料管理"
        context['title'] = u"物料管理"        
        return context  

class MaterialDetailView(SystemDetailView): 
    template_name = 'system/material_detail.html'
    context_object_name = 'material'
    model = Material
    def get_context_data(self, **kwargs): 
        context = super(MaterialDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"物料详细信息"
        context['title'] = u"物料详细信息"
        return context
class MaterialCreateView(CreateView):
    form_class= MaterialForm
    model = Material
    def get_context_data(self, **kwargs):
        context = super(MaterialCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"物料详细信息"
        context['title'] = u"物料详细信息"
        return context
    success_url =  reverse_lazy("material_list")
        
class MaterialUpdateView(UpdateView):
    form_class= MaterialForm
    model = Material
    success_url =  reverse_lazy("material_list")
    
class MaterialDeleteView(DeleteView):
    form_class= MaterialForm
    model = Material     
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        material = self.get_object(); 
        material.status = 0
        material.save() 
        return redirect('material_list');
        
          
#--------------------------------------------------工艺管理 界面定义------------------------------------------------------------------   
from system.models import Process, ProcessForm

class ProcessListView(SystemListView): 
    template_name = 'system/process_list.html'
    context_object_name = 'process_list'
    model = Process
    paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(ProcessListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"工艺管理"
        context['title'] = u"工艺管理"        
        return context  

class ProcessDetailView(SystemDetailView): 
    template_name = 'system/process_detail.html'
    context_object_name = 'process'
    model = Process
    def get_context_data(self, **kwargs): 
        context = super(ProcessDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"工艺详细信息"
        context['title'] = u"工艺详细信息"
        return context
class ProcessCreateView(CreateView):
    form_class= ProcessForm
    model = Process
    def get_context_data(self, **kwargs):
        context = super(ProcessCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"创建工艺信息"
        context['title'] = u"创建工艺信息"
        return context
    success_url =  reverse_lazy("process_list")
        
class ProcessUpdateView(UpdateView):
    form_class= ProcessForm
    model = Process
    success_url =  reverse_lazy("process_list")
    
class ProcessDeleteView(DeleteView):
    form_class= ProcessForm
    model = Process     
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        process = self.get_object(); 
        process.status = 0
        process.save() 
        return redirect('process_list');
   
#--------------------------------------------------班次管理 界面定义------------------------------------------------------------------   
from system.models import WorkClass, WorkClassForm

class WorkClassListView(SystemListView): 
    template_name = 'system/workclass_list.html'
    context_object_name = 'workclass_list'
    model = WorkClass
    paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(WorkClassListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"班次管理"
        context['title'] = u"班次管理"        
        return context  

class WorkClassDetailView(SystemDetailView): 
    template_name = 'system/workclass_detail.html'
    context_object_name = 'workclass'
    model = WorkClass
    def get_context_data(self, **kwargs): 
        context = super(WorkClassDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"班次详细信息"
        context['title'] = u"班次详细信息"
        return context
class WorkClassCreateView(CreateView):
    form_class= WorkClassForm
    model = WorkClass
    def get_context_data(self, **kwargs):
        context = super(WorkClassCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"创建班次信息"
        context['title'] = u"创建班次信息"
        return context
    success_url =  reverse_lazy("workclass_list")
        
class WorkClassUpdateView(UpdateView):
    form_class= WorkClassForm
    model = WorkClass
    success_url =  reverse_lazy("workclass_list")
    
class WorkClassDeleteView(DeleteView):
    form_class= WorkClassForm
    model = WorkClass     
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        workclass = self.get_object(); 
        workclass.status = 0
        workclass.save() 
        return redirect('workclass_list');



 
#--------------------------------------------------计件工资参数管理 界面定义------------------------------------------------------------------   
from system.models import SalaryCountConfig, SalaryCountConfigForm

class SalaryCountConfigListView(SystemListView): 
    template_name = 'system/salarycountconfig_list.html'
    context_object_name = 'salarycountconfig_list'
    model = SalaryCountConfig
    paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(SalaryCountConfigListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"计件工资管理"
        context['title'] = u"计件工资管理"        
        return context  

class SalaryCountConfigDetailView(SystemDetailView): 
    template_name = 'system/salarycountconfig_detail.html'
    context_object_name = 'salarycount'
    model = SalaryCountConfig
    def get_context_data(self, **kwargs): 
        context = super(SalaryCountConfigDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"计件工资详细信息"
        context['title'] = u"计件工资详细信息"
        return context
class SalaryCountConfigCreateView(CreateView):
    form_class= SalaryCountConfigForm
    model = SalaryCountConfig
    def get_context_data(self, **kwargs):
        context = super(SalaryCountConfigCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"创建计件工资信息"
        context['title'] = u"创建计件工资信息"
        return context
    success_url =  reverse_lazy("salarycount_list")
        
class SalaryCountConfigUpdateView(UpdateView):
    form_class= SalaryCountConfigForm
    model = SalaryCountConfig
    success_url =  reverse_lazy("salarycount_list")
    
class SalaryCountConfigDeleteView(DeleteView):
    form_class= SalaryCountConfigForm
    model = SalaryCountConfig     
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        salarycountconfig = self.get_object(); 
        salarycountconfig.status = 0
        salarycountconfig.save() 
        return redirect('salarycount_list');


#--------------------------------------------------计件工资参数管理 界面定义------------------------------------------------------------------   
from system.models import SalaryTimeConfig, SalaryTimeConfigForm

class SalaryTimeConfigListView(SystemListView): 
    template_name = 'system/salarytimeconfig_list.html'
    context_object_name = 'salarytimeconfig_list'
    model = SalaryTimeConfig
    paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(SalaryTimeConfigListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"计件工资管理"
        context['title'] = u"计件工资管理"        
        return context  

class SalaryTimeConfigDetailView(SystemDetailView): 
    template_name = 'system/salarytimeconfig_detail.html'
    context_object_name = 'salarytime'
    model = SalaryTimeConfig
    def get_context_data(self, **kwargs): 
        context = super(SalaryTimeConfigDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"计时工资详细信息"
        context['title'] = u"计时工资详细信息"
        return context
class SalaryTimeConfigCreateView(CreateView):
    form_class= SalaryTimeConfigForm
    model = SalaryTimeConfig
    def get_context_data(self, **kwargs):
        context = super(SalaryTimeConfigCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"创建计时工资信息"
        context['title'] = u"创建计时工资信息"
        return context
    success_url =  reverse_lazy("salarytime_list")
        
class SalaryTimeConfigUpdateView(UpdateView):
    form_class= SalaryTimeConfigForm
    model = SalaryTimeConfig
    success_url =  reverse_lazy("salarytime_list")
    
class SalaryTimeConfigDeleteView(DeleteView):
    form_class= SalaryTimeConfigForm
    model = SalaryTimeConfig     
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        salarytimeconfig = self.get_object(); 
        salarytimeconfig.status = 0
        salarytimeconfig.save() 
        return redirect('salarytime_list');

