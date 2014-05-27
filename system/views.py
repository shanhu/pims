# -*- coding: utf-8 -*- 
from django.views import generic
from django.views.generic.edit import FormMixin
from django import forms
import json
from django.db.models   import Q
from django.http import HttpResponse
from django.contrib import messages
from django.db import IntegrityError



# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
 
    
class IndexView(generic.ListView):
    template_name = 'system/developing.html'
    context_object_name = 'latest_materialType_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return MaterialType.objects.order_by('id')[:5] 


class SystemListView(generic.ListView, FormMixin):
    #template_name = 'system/base_list.html'
    #todo add dynamic menus here!
    paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(SystemListView, self).get_context_data(**kwargs)  
        context['pageHeader'] =  u"列表页"
        context['queryString'] = self.get_query_string().urlencode() 
        context['form'] = self.get_form_class()(self.request.GET)
        logger.info(self.request.GET.get('num'))
       
        return context
    def get_query_string(self):
        q = self.request.GET.copy() 
        logger.info(q)
        logger.info(self.request.GET)
        if q.__contains__('page'):
            q.pop('page')
        logger.info(" queryString = %s", q.urlencode())
        return q
    def get_queryset(self,**kwargs):
        if self.model:
            return self.model.objects.filter(**{key : self.request.GET[key] for key in self.request.GET  if  self.request.GET[key] <> '' and  key <> 'page' })
        
        
class SystemDetailView(generic.DetailView):
    template_name = 'system/base_detail.html'
    #todo add dynamic menus here!
    def get_context_data(self, **kwargs): 
        context = super(SystemDetailView, self).get_context_data(**kwargs) 
        context['menu_list'] = [] 
        context['breadcrumb'] = []
        return context

#--------------------------------------------------员工管理 界面定义------------------------------------------------------------------
from system.models import Employee, EmployeeForm,  NormalSearchForm, EmployeeSearchForm
class EmployeeListView(SystemListView): 
    template_name = 'system/employee_list.html'
    context_object_name = 'employee_list'
    model = Employee
    form_class = EmployeeSearchForm
    #paginate_by = 10
    
    def get_context_data(self, **kwargs): 
        context = super(EmployeeListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"员工汇总"
        context['title'] = u"员工汇总"
        context['sidebar'] = {'employee_list':'active'}
        context['add_url'] = reverse_lazy('employee_add')
        return context
    
    
class EmployeeDetailView(SystemDetailView): 
    template_name = 'system/employee_detail.html'
    context_object_name = 'employee'
    model = Employee 
    def get_context_data(self, **kwargs): 
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"员工详细信息"
        context['title'] = u"员工详细信息"
        context['sidebar'] = {'employee_list':'active'}
        return context 

from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

class EmployeeCreateView(CreateView):
    form_class = EmployeeForm
    model = Employee
    success_url =  reverse_lazy("employee_list")
    def get_context_data(self, **kwargs):
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"员工注册"
        context['title'] = u"员工注册"
        context['sidebar'] = {'employee_add':'active'}
        return context
    def post(self, request, *args, **kwargs):
        result = super(EmployeeCreateView, self).post(request, *args, **kwargs)  
        object = self.object
        logger.info('employee create: %s', object)
        if object:
            if object.card_num1:
                #employee_card = Card.objects.get(pk=object.card_num1)
                Card.objects.filter(num=object.card_num1).update(owner_id=object.id)
            if object.card_num2:
               # work_card = Card.objects.get(pk=object.card_num2)
                Card.objects.filter(num=object.card_num2).update(owner_id=object.id)
            if object.status == '0': 
                messages.warning(request,u'已分配卡片将被收回.')
        return result
         
class EmployeeUpdateView(UpdateView):
    form_class= EmployeeForm
    model = Employee
    success_url =  reverse_lazy("employee_list")
    def get_context_data(self, **kwargs):
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.fields['card_num1'].choices += [(self.object.card_num1,self.object.card_num1 )]
        form.fields['card_num2'].choices += [(self.object.card_num2,self.object.card_num2 )]
        context['form'] = form
        context['pageHeader'] = u"员工修改"
        context['title'] = u"员工修改"
        context['sidebar'] = {'employee_list':'active'}
        return context
    def post(self, request,  *args, **kwargs):
        object = self.get_object()
        Card.objects.retriveCards(num= object.card_num1)
        Card.objects.retriveCards(num= object.card_num2)
        result = super(EmployeeUpdateView, self).post(request, *args, **kwargs)        
        object = self.object 
        if object.status == '0': 
            messages.success(request, u" %s 已经离职，卡片 %s %s 已被收回！" % (self.object.name, self.object.card_num1, self.object.card_num2) )
            Card.objects.retriveCards( num= object.card_num1)
            Card.objects.retriveCards( num= object.card_num2)
            object.card_num1 = ''
            object.card_num2 = ''
            object.save()
        else:
            Card.objects.grantCards(num= object.card_num1, owner_id = object.id)
            Card.objects.grantCards(num= object.card_num2, owner_id = object.id)
        
        
        return result #redirect('employee_list')
    
class EmployeeDeleteView(DeleteView):
    form_class= EmployeeForm
    model = Employee     
    success_url = reverse_lazy('employee_list')  
    def post(self,request, *args, **kwargs): 
        try:
            result =  super(EmployeeDeleteView, self).post(request, *args, **kwargs)
            messages.success(request, u" %s 已被删除，卡片 %s %s 已被收回！" % (self.object.name, self.object.card_num1, self.object.card_num2) )
            employee = self.object; 
            if employee.card_num1 != '' or employee.card_num2 != '':
                Card.objects.retriveCards(num= employee.card_num1)
                Card.objects.retriveCards(num= employee.card_num2)
            return result
        except(IntegrityError):
            messages.error(request, u" %s 已被使用，不能删除" % self.object.name)  
          
        return redirect('employee_list');
    def get_context_data(self, **kwargs):
        context = super(EmployeeDeleteView, self).get_context_data(**kwargs)   
        context['sidebar'] = {'employee_list':'active'}
        return context 
            
#--------------------------------------------------物料类型管理 界面定义------------------------------------------------------------------   
from system.models import MaterialType, MaterialTypeForm

class MaterialTypeListView(SystemListView): 
    template_name = 'system/materialType_list.html'
    context_object_name = 'materialType_list'
    model = MaterialType
    form_class = NormalSearchForm
    #paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(MaterialTypeListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"物料类型管理"
        context['title'] = u"物料类型管理"
        context['sidebar'] = {'material_type':'active'}    
        context['add_url'] = reverse_lazy('material_type_add')
        return context  

class MaterialTypeDetailView(SystemDetailView): 
    template_name = 'system/materialType_detail.html'
    context_object_name = 'materialType'
    model = MaterialType
    def get_context_data(self, **kwargs): 
        context = super(MaterialTypeDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"物料类型详细信息"
        context['title'] = u"物料类型详细信息"
        context['sidebar'] = {'material_type':'active'}   
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
        context['sidebar'] = {'material_type':'active'}   
        return context
    success_url =  reverse_lazy("material_type_list")
        
class MaterialTypeUpdateView(UpdateView):
    form_class= MaterialTypeForm
    model = MaterialType
    success_url =  reverse_lazy("material_type_list")
    def get_context_data(self, **kwargs):
        context = super(MaterialTypeUpdateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"物料类型修改"
        context['title'] = u"物料类型修改"
        context['sidebar'] = {'material_type':'active'}   
        return context
    
class MaterialTypeDeleteView(DeleteView):
    form_class= MaterialTypeForm
    model = MaterialType     
    success_url = reverse_lazy('material_type_list') 
    def post(self,request, *args, **kwargs):
        try:
             result = super(MaterialTypeDeleteView, self).post(request, *args, **kwargs)
             messages.success(request, u"物料类型已被成功删除！" )
             return result
        except(IntegrityError):
            messages.error(request, u"物料类型已被使用，不能删除") 
        else:
            materialType = self.get_object()
            materialType.status = 0
            materialType.save() 
        return redirect('material_type_list')
        
    def get_context_data(self, **kwargs):
        context = super(MaterialTypeDeleteView, self).get_context_data(**kwargs)  
        context['sidebar'] = {'material_type':'active'}   
        return context
           
#--------------------------------------------------物料管理 界面定义------------------------------------------------------------------   
from system.models import Material, MaterialForm

class MaterialListView(SystemListView): 
    template_name = 'system/material_list.html'
    context_object_name = 'material_list'
    model = Material
    form_class=NormalSearchForm
    #paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(MaterialListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"物料管理"
        context['title'] = u"物料管理"  
        context['sidebar'] = {'material':'active'}  
        context['add_url'] = reverse_lazy('material_add')  
        return context  

class MaterialDetailView(SystemDetailView): 
    template_name = 'system/material_detail.html'
    context_object_name = 'material'
    model = Material
    def get_context_data(self, **kwargs): 
        context = super(MaterialDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"物料详细信息"
        context['title'] = u"物料详细信息"
        context['sidebar'] = {'material':'active'} 
        return context
class MaterialCreateView(CreateView):
    form_class= MaterialForm
    model = Material
    def get_context_data(self, **kwargs):
        context = super(MaterialCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form
        cardTypeChoices =  Card.getCardChoices(type="3")
        logger.info("material card type choices: %s", cardTypeChoices )
        form.fields['card_num'] = forms.ChoiceField(   choices=cardTypeChoices ,  label="物料卡编号", required=False )
        context['pageHeader'] = u"物料详细信息"
        context['title'] = u"物料详细信息"
        context['sidebar'] = {'material':'active'} 
        return context
    def post(self, request, **kwargs):
        result = super(MaterialCreateView, self).post(request, **kwargs)
        object = self.object
        if object:
            Card.objects.filter(num=object.card_num).update(owner_id=object.id)
        return result
    success_url =  reverse_lazy("material_list")
        
class MaterialUpdateView(UpdateView):
    form_class= MaterialForm
    model = Material
    success_url =  reverse_lazy("material_list")
    def get_context_data(self, **kwargs):
        context = super(MaterialUpdateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form
        if self.object.card_num:
            cardTypeChoices = [(self.object.card_num,self.object.card_num  ) ]  + Card.getCardChoices(type="3") + [('', '-------')]
        else:
            cardTypeChoices = Card.getCardChoices(type="3") + [('', '-------')]
        logger.info("material card type choices: %s", cardTypeChoices )
        form.fields['card_num'] = forms.ChoiceField(   choices=cardTypeChoices ,  label="物料卡编号", required=False )
        context['pageHeader'] = u"物料详细信息"
        context['title'] = u"物料详细信息"
        context['sidebar'] = {'material':'active'} 
        return context
    def post(self, request, **kwargs):
        object = self.get_object()
        Card.objects.filter(num=object.card_num).update(owner_id='0')
        result = super(MaterialUpdateView, self).post(request, **kwargs)
        
        if self.object.status == '1':
            Card.objects.filter(num=self.object.card_num).update(owner_id=self.object.id)
            if self.object.card_num:
                messages.success(request, u" %s 可用，卡片 %s 已下发！" % (self.object.name, self.object.card_num) )
            else:
                messages.success(request, u" %s 可用，卡片 %s 已被收回！" % (self.object.name, object.card_num) )
        else:
            messages.success(request, u" %s 已不可用，卡片 %s 已被收回！" % (self.object.name, self.object.card_num) )
            Card.objects.retriveCards(num=object.card_num)
            object.card_num = ''
            object.save()
            
        return result;
class MaterialDeleteView(DeleteView):
    form_class= MaterialForm
    model = Material     
    success_url = reverse_lazy('material_list')  
    def post(self,request, *args, **kwargs):
        try:
            result = super(MaterialDeleteView, self).post(request, *args, **kwargs)
            Card.objects.retriveCards(type='3', num=self.object.card_num)
            messages.success(request, u"物料删除成功！") 
            return result
        except(IntegrityError):
            messages.error(request, u"物料已被使用，不能删除")  
        return redirect('material_list');
    def get_context_data(self, **kwargs):
        context = super(MaterialDeleteView, self).get_context_data(**kwargs) 
        context['sidebar'] = {'material':'active'} 
        return context    
          
#--------------------------------------------------工艺管理 界面定义------------------------------------------------------------------   
from system.models import Process, ProcessForm

class ProcessListView(SystemListView): 
    template_name = 'system/process_list.html'
    context_object_name = 'process_list'
    model = Process
    form_class = NormalSearchForm
    #paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(ProcessListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"工艺管理"
        context['title'] = u"工艺管理" 
        context['sidebar'] = {'process':'active'}    
        context['add_url'] = reverse_lazy("process_add")
        return context

class ProcessDetailView(SystemDetailView): 
    template_name = 'system/process_detail.html'
    context_object_name = 'process'
    model = Process
    def get_context_data(self, **kwargs): 
        context = super(ProcessDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"工艺详细信息"
        context['title'] = u"工艺详细信息"
        context['sidebar'] = {'process':'active'} 
        return context
class ProcessCreateView(CreateView):
    form_class= ProcessForm
    model = Process
    success_url =  reverse_lazy("process_list")
    def get_context_data(self, **kwargs):
        context = super(ProcessCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"创建工艺信息"
        context['title'] = u"创建工艺信息"
        context['sidebar'] = {'process':'active'} 
        return context
    def post(self, request, **kwargs):
        result = super(ProcessCreateView, self).post(request, **kwargs)
        object = self.object
        Card.objects.filter(num=object.card_num).update(owner_id=object.id)
        return result 
    
        
class ProcessUpdateView(UpdateView):
    form_class= ProcessForm
    model = Process
    success_url =  reverse_lazy("process_list")
    def get_context_data(self, **kwargs):
        context = super(ProcessUpdateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form
        context['pageHeader'] = u"修改工艺信息"
        context['title'] = u"修改工艺信息"
        context['sidebar'] = {'process':'active'} 
        form.fields['card_num'].choices += [(self.object.card_num,self.object.card_num )]
        return context
    def post(self, request, **kwargs):
        object = self.get_object()
        Card.objects.retriveCards(num=object.card_num)
        result = super(ProcessUpdateView, self).post(request, **kwargs)
        object = self.object
        if object.status == '0':
            messages.success(request, u" %s 流程已不可用，卡片 %s 已被收回！" % (self.object.name, self.object.card_num) )
        else:
            Card.objects.grantCards(num=object.card_num,owner_id=object.id)
            messages.success(request, u"新卡片 %s 已被分配！" % (self.object.name, self.object.card_num) )
        return result;
    
class ProcessDeleteView(DeleteView):
    form_class= ProcessForm
    model = Process     
    success_url = reverse_lazy('process_list')  
    def post(self,request, *args, **kwargs):
        try:
            result = super(ProcessDeleteView, self).post(request, *args, **kwargs)
            object = self.object
            Card.objects.retriveCards(num=object.card_num)
            messages.success(request, u"工艺已被成功删除！")  
            return result
        except(IntegrityError):
            messages.error(request, u"工艺已被使用，不能删除！")  
        return redirect('process_list');
    def get_context_data(self, **kwargs):
        context = super(ProcessDeleteView, self).get_context_data(**kwargs) 
        context['sidebar'] = {'process':'active'} 
        return context
#--------------------------------------------------班次管理 界面定义------------------------------------------------------------------   
from system.models import WorkClass, WorkClassForm

class WorkClassListView(SystemListView): 
    template_name = 'system/workclass_list.html'
    context_object_name = 'workclass_list'
    model = WorkClass
    #paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(WorkClassListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"班次管理"
        context['title'] = u"班次管理" 
        context['sidebar'] = {'process':'active'}        
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
from system.models import SalaryCountConfig, SalaryCountConfigForm, SalaryCountSearchForm

class SalaryCountConfigListView(SystemListView): 
    template_name = 'system/salarycountconfig_list.html'
    context_object_name = 'salarycountconfig_list'
    model = SalaryCountConfig
    form_class = SalaryCountSearchForm
    #paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(SalaryCountConfigListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"计件工资管理"
        context['title'] = u"计件工资管理"  
        context['sidebar'] = {'salary_count_config':'active'}
        context['add_url'] = reverse_lazy('salarycount_add')    
        return context  

class SalaryCountConfigDetailView(SystemDetailView): 
    template_name = 'system/salarycountconfig_detail.html'
    context_object_name = 'salarycount'
    model = SalaryCountConfig
    def get_context_data(self, **kwargs): 
        context = super(SalaryCountConfigDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"计件工资详细信息"
        context['title'] = u"计件工资详细信息"
        context['sidebar'] = {'salary_count_config':'active'}   
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
        context['sidebar'] = {'salary_count_config':'active'}   
        return context
    success_url =  reverse_lazy("salarycount_list")
        
class SalaryCountConfigUpdateView(UpdateView):
    form_class= SalaryCountConfigForm
    model = SalaryCountConfig
    success_url =  reverse_lazy("salarycount_list")
    def get_context_data(self, **kwargs):
        context = super(SalaryCountConfigUpdateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"修改计件工资信息"
        context['title'] = u"修改计件工资信息"
        context['sidebar'] = {'salary_count_config':'active'}   
        return context
    
class SalaryCountConfigDeleteView(DeleteView):
    form_class= SalaryCountConfigForm
    model = SalaryCountConfig     
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        salarycountconfig = self.get_object(); 
        salarycountconfig.status = 0
        salarycountconfig.save() 
        return redirect('salarycount_list');
    def get_context_data(self, **kwargs):
        context = super(SalaryCountConfigDeleteView, self).get_context_data(**kwargs) 
        context['sidebar'] = {'salary_count_config':'active'}   
        return context


#--------------------------------------------------计件工资参数管理 界面定义------------------------------------------------------------------   
from system.models import SalaryTimeConfig, SalaryTimeConfigForm

class SalaryTimeConfigListView(SystemListView): 
    template_name = 'system/salarytimeconfig_list.html'
    context_object_name = 'salarytimeconfig_list'
    model = SalaryTimeConfig
    form_class = SalaryTimeConfigForm
    #paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(SalaryTimeConfigListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"计件工资管理"
        context['title'] = u"计件工资管理"
        context['sidebar'] = {'salary_time_config':'active'}
        context['add_url'] = reverse_lazy('salarytime_add')        
        return context  

class SalaryTimeConfigDetailView(SystemDetailView): 
    template_name = 'system/salarytimeconfig_detail.html'
    context_object_name = 'salarytime'
    model = SalaryTimeConfig
    def get_context_data(self, **kwargs): 
        context = super(SalaryTimeConfigDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"计时工资详细信息"
        context['title'] = u"计时工资详细信息"
        context['sidebar'] = {'salary_time_config':'active'} 
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
        context['sidebar'] = {'salary_time_config':'active'} 
        return context
    success_url =  reverse_lazy("salarytime_list")
        
class SalaryTimeConfigUpdateView(UpdateView):
    form_class= SalaryTimeConfigForm
    model = SalaryTimeConfig
    success_url =  reverse_lazy("salarytime_list")
    def get_context_data(self, **kwargs):
        context = super(SalaryTimeConfigUpdateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"修改计时工资信息"
        context['title'] = u"修改计时工资信息"
        context['sidebar'] = {'salary_time_config':'active'} 
        return context
    
class SalaryTimeConfigDeleteView(DeleteView):
    form_class= SalaryTimeConfigForm
    model = SalaryTimeConfig     
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        salarytimeconfig = self.get_object(); 
        salarytimeconfig.status = 0
        salarytimeconfig.save() 
        return redirect('salarytime_list');
    def get_context_data(self, **kwargs):
        context = super(SalaryTimeConfigDeleteView, self).get_context_data(**kwargs) 
        context['sidebar'] = {'salary_time_config':'active'} 
        return context


#--------------------------------------------------卡片管理 界面定义------------------------------------------------------------------   
from system.models import Card, CardForm, CardSearchForm

class CardListView(SystemListView): 
    template_name = 'system/card_list.html'
    context_object_name = 'card_list'
    model = Card
    form_class = CardSearchForm
    #paginate_by = 10
    logger.info("system out test.")
    def get_context_data(self, **kwargs): 
        context = super(CardListView, self).get_context_data(**kwargs)  
        #form_class = self.get_form_class()
        logger.info("form info %s ", context['form'])
        context['pageHeader'] = u"卡管理"
        context['title'] = u"卡管理"
        context['sidebar'] = {'card':'active'}
        context['add_url'] = reverse_lazy('card_add')
        context['is_display'] = 'none'
        return context
    def get_queryset(self):
        type = self.request.GET.get('type')
        logger.info("request params type is %s", type)
        q = self.get_query_string()
        return Card.objects.searchCards(q)  
       # logger.info("1111%request",  self.request) 
    def get_success_url(self):
        return reverse_lazy('card_list', kwargs={'pk': self.object.pk}) 
        
class CardDetailView(SystemDetailView): 
    template_name = 'system/card_detail.html'
    context_object_name = 'card'
    model = Card
    def get_context_data(self, **kwargs): 
        context = super(CardDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"卡详细信息"
        context['title'] = u"卡详细信息"
        context['sidebar'] = {'card':'active'} 
        return context
    
   
    
class CardCreateView(CreateView):
    form_class= CardForm
    model = Card
    def get_context_data(self, **kwargs):
        context = super(CardCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"创建卡关联信息"
        context['title'] = u"创建卡关联信息"
        context['sidebar'] = {'card':'active'} 
     
        return context
    success_url =  reverse_lazy("card_list")
    def get(self,request,  *args, **kwargs):
        if request.is_ajax():
            return self.render_to_json_response(request, *args, **kwargs)
        else:
           return super(CreateView, self).get(request, *args, **kwargs)
            
        
    def render_to_json_response(self, context, **response_kwargs):
        logger.info(self.get_object().__dict__)
        data = self.get_object().__dict__
        del data['_state'] 
        data = json.dumps(data)
        logger.info(data)
        #response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, content_type='application/json')
        
class CardUpdateView(UpdateView):
    form_class= CardForm
    model = Card
    success_url =  reverse_lazy("card_list")
    def get_context_data(self, **kwargs):
        context = super(CardUpdateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        logger.info("card form: %s", form_class)
        logger.info(self.get_object())
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"修改卡关联信息"
        context['title'] = u"修改卡关联信息"
        context['sidebar'] = {'card':'active'} 
        return context
    def get(self,request,  *args, **kwargs):
        if request.is_ajax():
            return self.render_to_json_response(request, *args, **kwargs)
        else:
           return super(CardUpdateView, self).get(request, *args, **kwargs)
    def post(self,*args, **kwargs):
        card = self.get_object()
        logger.info("owner id is %s" ,  card.owner_id )
        owner_id = card.owner_id
        result = super(CardUpdateView, self).post(*args, **kwargs)
        self.update_card_owner(owner_id)
        card = self.object
       # logger.info(form)
        return result #redirect('card_list');
    def update_card_owner(self, owner_id):
        card = self.object
        owner_getter = {'1': WorkClass.objects, '2':WorkClass.objects, '3':Material.objects, '4':Process.objects, '5':Employee.objects, '6':Employee.objects}
        
        if card.owner_id:
            owner = owner_getter.get(card.type).get(pk = card.owner_id)
            if card.type == '5':
                owner.card_num1 = card.num
            elif card.type == '6':
                owner.card_num2 = card.num
            else:
                owner.card_num = card.num
            owner.save()
        elif owner_id:
            owner = owner_getter.get(card.type).get(pk = owner_id)
            if card.type == '5':
                owner.card_num1 = ''
            elif card.type == '6':
                owner.card_num2 = ''
            else:
                owner.card_num = ''
            owner.save()
        
    def render_to_json_response(self, context, **response_kwargs):
        logger.info(self.get_object().__dict__)
        data = self.get_object().__dict__
        del data['_state'] 
        data = json.dumps(data)
        logger.info(data)
        #response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, content_type='application/json')
    def get_form(self,form_class):
        form = super(CardUpdateView, self).get_form(form_class)
      #  logger.info(" object: %s", self.get_object() )        
      #  logger.info( u"form running times: %s   type : %s ", form, self.get_object().type ) 
        form = self.update_type_field(form)
      #  logger.info("%s", form)
        return form
   
    def getProcess(self,  form,  **kwargs):
        process = [(0, '---------')] + [ (process.id, u" 编号(%s)  名称(%s)  工艺卡号(%s)" % (process.num, process.name, process.card_num) ) for process in Process.objects.filter(Q(card_num__isnull=True) | Q(card_num='') | Q( pk = self.get_object().owner_id))]
        logger.info("process %s ", process)
        form.fields['owner_id'] = forms.IntegerField(widget=forms.Select( choices= process), label="工艺" , required=False)
        return  form
    def getEmployee(self, form, **kwargs):
        query = Employee.objects.filter()
        if kwargs['type'] == '5' :
          query =  query.filter(Q(card_num1__isnull=True) | Q(card_num1='') )
        if kwargs['type'] == '6':
          query =  query.filter(Q(card_num2__isnull=True) | Q(card_num2='') )
        employees = [(0, '---------')] + [( employee.id, u"编号:(%s) 姓名:(%s) 身份证:(%s) " % (employee.num , employee.name, employee.idCard) ) for employee in query ] + Employee.getTypeChoices(pk=self.object.owner_id)
        form.fields['owner_id'] = forms.IntegerField(widget=forms.Select( choices= employees), label="员工" , required=False)
        return form
    def getWorkClass(self,form,  **kwargs):
        query = WorkClass.objects.filter() 
        logger.info('type %r' ,  kwargs)
        if kwargs['type'] == '1' :
           query = query.filter(Q(type='0'), Q(card_num__isnull=True) | Q(card_num='')) 
        if kwargs['type'] == '2':
           query =  query.filter(Q(type='1'), Q(card_num__isnull=True)  | Q(card_num=''))
        workclazz = [(0, '---------')] + [(workclass.id, workclass.name )for workclass in query] 
        if self.object.owner_id:            
            workclazz += WorkClass.getTypeChoices(pk = self.object.owner_id)
        #logger.info('workclass %s', workclazz)
        form.fields['owner_id'] = forms.IntegerField(widget=forms.Select( choices= workclazz), label="班次" , required=False)
        return form
 
    def getMaterial(self,form, **kwargs):
        materials = [(0, '---------')] + [(material.id, material.name) for material in Material.objects.filter(Q(card_num__isnull=True) | Q(card_num='') )]
        form.fields['owner_id'] = forms.IntegerField(widget=forms.Select( choices= materials), label="物料" , required=False)
        return form
    def update_type_field(self, form):
        obj = self.get_object()
        type = obj.type
        logger.info("card:%s", obj)
        form_updater = {'1':self.getWorkClass, '2':self.getWorkClass, '3':self.getMaterial, '4':self.getProcess, '5':self.getEmployee, '6':self.getEmployee}
        form = form_updater.get(type)( form, type=type) 
        return form
class CardDeleteView(DeleteView):
    form_class= CardForm
    model = Card     
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        card = self.get_object(); 
        card.status = 0
        
        return redirect('card_list');
    def get_context_data(self, **kwargs):
        context = super(CardDeleteView, self).get_context_data(**kwargs) 
        context['sidebar'] = {'card':'active'} 
        return context


#--------------------------------------------------实时数据 界面定义------------------------------------------------------------------   
from system.models import Production, ProductionSearchForm
class ProductionListView(SystemListView):
    template_name = 'system/production_list.html'
    context_object_name = 'production_list'
    model = Production
    form_class = ProductionSearchForm
    #paginate_by = 10
    logger.info("system out test.") 
    def get_context_data(self, *args, **kwargs):
        context = super(ProductionListView, self).get_context_data(*args, **kwargs)
        context['pageHeader'] = u"实时生产数据"
        context['title'] = u"数据中心"
        return context
    def get_queryset(self):
        querySql = '''
            SELECT ROWNUM ID,PROCESS_ID,FIRST_PROCESS_NAME,SECOND_PROCESS_NAME,MATERIAL_ID,EMPLOYEE_NUM, EMPLOYEE_NAME, MATERIAL_NUM, MATERIAL_NAME, START_COUNT, STARTTIME, END_COUNT, ENDTIME, OUT_RATE FROM (
                    SELECT TMP.* ,
                    IF(TMP.BPD_ID = @BPD_ID, @RANK:=@RANK+1,@RANK:=1) RANK,
                     @BPD_ID := TMP.BPD_ID,
                     @ROWNUM := @ROWNUM + 1 ROWNUM
                    FROM (
                    SELECT APD.PROCESS_ID PROCESS_ID,APD.EMPLOYEE_ID EMPLOYEE_ID,APD.CARD_ID CARD_ID, BPS.NAME FIRST_PROCESS_NAME,APS.NAME SECOND_PROCESS_NAME, APD.MATERIAL_ID MATERIAL_ID, BPD.ID BPD_ID , E.NUM EMPLOYEE_NUM ,E.NAME EMPLOYEE_NAME ,M.NUM MATERIAL_NUM ,M.NAME MATERIAL_NAME ,BPD.COUNT START_COUNT ,BPD.TIME STARTTIME ,IFNULL(APD.COUNT,BPD.COUNT) END_COUNT,IFNULL(APD.TIME,BPD.TIME) ENDTIME , ROUND(APD.COUNT  / IFNULL(BPD.COUNT,APD.COUNT) * 100,2) OUT_RATE
                      FROM PRODUCTION APD
                      JOIN EMPLOYEE E ON APD.EMPLOYEE_ID = E.ID
                      JOIN MATERIAL M ON APD.MATERIAL_ID = M.ID
                      JOIN PROCESS APS ON APD.PROCESS_ID = APS.ID AND  APS.IS_FIRST = 0
                      LEFT JOIN PROCESS BPS ON  APS.FIRST_PROCESS_ID = BPS.ID  AND  BPS.IS_FIRST = 1 
                      LEFT JOIN PRODUCTION BPD ON BPD.PROCESS_ID = BPS.ID  AND APD.MATERIAL_ID = BPD.MATERIAL_ID AND APD.EMPLOYEE_ID = BPD.EMPLOYEE_ID AND APD.CARD_ID = BPD.CARD_ID
                    WHERE IFNULL(BPD.TIME,APD.TIME - 1) < APD.TIME  
                    ORDER BY BPD.TIME , APD.TIME ) TMP,(SELECT @RANK,@ROWNUM:=0,@BPD_ID:= NULL ) T 
                    #ORDER BY EMPLOYEE_ID,CARD_ID,MATERIAL_ID  DESC
                ) PD
                WHERE PD.RANK = 1
               
        '''
        
        querySql = u'''         
            select pd.id ID, e.NUM EMPLOYEE_NUM,e.NAME EMPLOYEE_NAME ,m.NAME MATERIAL_NAME ,if(ps.IS_FIRST,'前','后') IS_FIRST,  ps.name PROCESS_NAME ,pd.COUNT START_COUNT ,pd.TIME START_TIME from production pd
            join process ps on pd.PROCESS_ID = ps.ID
            join material m on m.id = pd.MATERIAL_ID
            join employee e on e.ID = pd.EMPLOYEE_ID 
            WHERE 1=1
            
        '''
        
        if "employee_num" in self.request.GET:
            employee_num =  self.request.GET['employee_num']
            if employee_num:
                querySql += "and e.NUM = %s " % employee_num
        if "employee_name" in self.request.GET:
            employee_name =  self.request.GET['employee_name']
            if employee_name:
                querySql += "and e.NAME = '%s' " % employee_name
        if "process" in self.request.GET:
            process = self.request.GET['process']
            if process:
                querySql += "and PD.PROCESS_ID = '%s' " % process
        if "material" in self.request.GET:
            material = self.request.GET['material']
            if material:
                querySql += "and PD.MATERIAL_ID = '%s' " % material
        return list(Production.objects.raw(querySql   + "  order by   pd.time desc, pd.EMPLOYEE_ID ,pd.MATERIAL_ID "))
 
