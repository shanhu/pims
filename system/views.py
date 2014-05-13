# -*- coding: utf-8 -*- 
from django.views import generic
from django.views.generic.edit import FormMixin
from django import forms
import json
from django.db.models   import Q
from django.http import HttpResponse

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
        context['sidebar'] = {'employee_list':'active'}
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
    form_class= EmployeeForm
    model = Employee
    def get_context_data(self, **kwargs):
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"员工注册"
        context['title'] = u"员工注册"
        context['sidebar'] = {'employee_add':'active'}
        return context
        
class EmployeeUpdateView(UpdateView):
    form_class= EmployeeForm
    model = Employee 
    def get_context_data(self, **kwargs):
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"员工修改"
        context['title'] = u"员工修改"
        context['sidebar'] = {'employee_list':'active'}
        return context
    
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
    paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(MaterialTypeListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"物料类型管理"
        context['title'] = u"物料类型管理"
        context['sidebar'] = {'material_type':'active'}        
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
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        materialType = self.get_object(); 
        materialType.status = 0
        materialType.save() 
        return redirect('material_type_list');
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
    paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(MaterialListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"物料管理"
        context['title'] = u"物料管理"  
        context['sidebar'] = {'material':'active'}       
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
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"物料详细信息"
        context['title'] = u"物料详细信息"
        context['sidebar'] = {'material':'active'} 
        return context
    success_url =  reverse_lazy("material_list")
        
class MaterialUpdateView(UpdateView):
    form_class= MaterialForm
    model = Material
    success_url =  reverse_lazy("material_list")
    def get_context_data(self, **kwargs):
        context = super(MaterialUpdateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"物料详细信息"
        context['title'] = u"物料详细信息"
        context['sidebar'] = {'material':'active'} 
        return context
class MaterialDeleteView(DeleteView):
    form_class= MaterialForm
    model = Material     
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        material = self.get_object(); 
        material.status = 0
        material.save() 
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
    paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(ProcessListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"工艺管理"
        context['title'] = u"工艺管理" 
        context['sidebar'] = {'process':'active'}        
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
    def get_context_data(self, **kwargs):
        context = super(ProcessCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"创建工艺信息"
        context['title'] = u"创建工艺信息"
        context['sidebar'] = {'process':'active'} 
        return context
    success_url =  reverse_lazy("process_list")
        
class ProcessUpdateView(UpdateView):
    form_class= ProcessForm
    model = Process
    success_url =  reverse_lazy("process_list")
    def get_context_data(self, **kwargs):
        context = super(ProcessUpdateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"修改工艺信息"
        context['title'] = u"修改工艺信息"
        context['sidebar'] = {'process':'active'} 
        return context
    
class ProcessDeleteView(DeleteView):
    form_class= ProcessForm
    model = Process     
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        process = self.get_object(); 
        process.status = 0
        process.save() 
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
    paginate_by = 10
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
        context['sidebar'] = {'salary_count_config':'active'}       
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
    paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(SalaryTimeConfigListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"计件工资管理"
        context['title'] = u"计件工资管理"
        context['sidebar'] = {'salary_time_config':'active'}         
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

class CardListView(SystemListView, FormMixin): 
    template_name = 'system/card_list.html'
    context_object_name = 'card_list'
    model = Card
    form_class = CardSearchForm
    paginate_by = 10
    logger.info("system out test.")
    def get_context_data(self, **kwargs): 
        context = super(CardListView, self).get_context_data(**kwargs)  
        #form_class = self.get_form_class()
        context['form'] = CardSearchForm({'num':self.request.GET.get('num'), 
        'type':self.request.GET.get('type'), 
        'assignd':self.request.GET.get('assignd') }) 
        logger.info("form info %s ", context['form'])
        context['pageHeader'] = u"计件工资管理"
        context['title'] = u"计件工资管理"
        context['sidebar'] = {'card':'active'} 
        context['queryString'] = self.get_query_string().urlencode()
        return context
    def get_queryset(self):
        type = self.request.GET.get('type')
        logger.info("request params type is %s", type)
        q = self.get_query_string()
        query = Card.objects.filter()
        if q.get('type'):
            query = query.filter(type=q.get('type'))
        if q.get('assignd') == '0' :
            query = query.filter(owner_id__isnull = True)
        elif q.get('assignd') == '1' :
            query = query.filter(owner_id__isnull = False)
        if q.get('num'):
            query = query.filter(num=q.get('num'))
            
        return query
       # logger.info("1111%request",  self.request) 
    def get_success_url(self):
        return reverse_lazy('card_list', kwargs={'pk': self.object.pk})
    def get_query_string(self):
        q = self.request.GET.copy() 
        if q.__contains__('page'):
            q.pop('page')
        logger.info(" queryString = %s", q.urlencode())
        return q
        
class CardDetailView(SystemDetailView): 
    template_name = 'system/card_detail.html'
    context_object_name = 'card'
    model = Card
    def get_context_data(self, **kwargs): 
        context = super(CardDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"计时工资详细信息"
        context['title'] = u"计时工资详细信息"
        context['sidebar'] = {'card':'active'} 
        return context
        
   
    
class CardCreateView(CreateView):
    form_class= CardForm
    model = Card
    def get_context_data(self, **kwargs):
        context = super(CardCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        context['pageHeader'] = u"创建计时工资信息"
        context['title'] = u"创建计时工资信息"
        context['sidebar'] = {'card':'active'} 
        return context
    success_url =  reverse_lazy("card_list")
    def get(self,request,  *args, **kwargs):
        if request.is_ajax():
            return self.render_to_json_response(request, *args, **kwargs)
        else:
           return super(SystemDetailView, self).get(request, *args, **kwargs)
            
        
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
        context['pageHeader'] = u"修改计时工资信息"
        context['title'] = u"修改计时工资信息"
        context['sidebar'] = {'card':'active'} 
        return context
    def get(self,request,  *args, **kwargs):
        if request.is_ajax():
            return self.render_to_json_response(request, *args, **kwargs)
        else:
           return super(CardUpdateView, self).get(request, *args, **kwargs)
            
        
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
        logger.info(" object: %s", self.get_object() )        
        logger.info( u"form running times: %s   type : %s ", form, self.get_object().type ) 
        self.update_type_field(form)
        logger.info("%s", form)
        return form
   
    def getProcess(self, **kwargs):
        process = [('', '---------')] + [ (process.id, process.name) for process in Process.objects.filter(Q(card_num__isnull=True) | Q(card_num='') )]
        logger.info("process %s ", process)
        return  process
    def getEmployee(self, **kwargs):
        query = Employee.objects.filter()
        if kwargs['type'] == '5' :
            query.filter(Q(card_num1__isnull=True) | Q(card_num1='') )
        if kwargs['type'] == '6':
            query.filter(Q(card_num2__isnull=True) | Q(card_num2='') )
        return query
    def getWorkClass(self, **kwargs):
        query = WorkClass.objects.filter() 
        if kwargs['type'] == '1' :
            query.filter(Q(type='1'), Q(card_num__isnull=True) | Q(card_num=''))
        if kwargs['type'] == '2':
             query.filter(Q(type='1'), Q(card_num__isnull=True) | Q(card_num=''))
        return query
 
    def getMaterial(self, **kwargs):
        return Material.objects.filter(card_num__isnull=True,)
    def update_type_field(self, form):
        obj = self.get_object()
        type = obj.type
        logger.info("card:%s", obj)
        choices_produce = {'1':self.getWorkClass, '2':self.getWorkClass, '3':self.getMaterial, '4':self.getProcess, '5':self.getEmployee, '6':self.getEmployee}
        choices = choices_produce.get(type)(type=type)
        logger.info(" choices: %s ", choices)
        form.fields['owner_id'] = forms.CharField(widget=forms.Select( choices= choices), label="所有者")
        logger.info("form %s", form)
        return form
class CardDeleteView(DeleteView):
    form_class= CardForm
    model = Card     
    #success_url = reverse_lazy('material_type_list')  
    def post(self,*args, **kwargs):
        card = self.get_object(); 
        card.status = 0
        card.save() 
        return redirect('card_list');
    def get_context_data(self, **kwargs):
        context = super(CardDeleteView, self).get_context_data(**kwargs) 
        context['sidebar'] = {'card':'active'} 
        return context
