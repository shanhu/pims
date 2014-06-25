# -*- coding: utf-8 -*- 
from django.views import generic
from django.views.generic.edit import FormMixin
from django import forms
import json
from django.db.models   import Q
from django.http import HttpResponse
from django.contrib import messages
from django.db import IntegrityError
from django.core.cache import cache
from datetime import datetime


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
        return context
    def get_query_string(self):
        q = self.request.GET.copy() 
        #logger.info(q)
        #logger.info(self.request.GET)
        if q.__contains__('page'):
            q.pop('page')
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
        form = self.get_form(form_class) 
        #form.fields['cardprt1'].choices =   Card.getCardChoices(type='5')  
        #form.fields['cardprt2'].choices =   Card.getCardChoices(type='6')  
        context['form'] = form    
        context['pageHeader'] = u"员工注册"
        context['title'] = u"员工注册"
        context['sidebar'] = {'employee_add':'active'}
        return context
    def form_valid(self, form):
        response = super(EmployeeCreateView, self).form_valid(form)
        object = self.object
        logger.info('employee create: %s', object)
        ''' 外键关联方式，不需要额外验证。2014-06-08
        if object:
            if object.card_num1:
                #employee_card = Card.objects.get(pk=object.card_num1)
                Card.objects.filter(num=object.card_num1).update(owner_id=object.id)
            if object.card_num2:
               # work_card = Card.objects.get(pk=object.card_num2)
                Card.objects.filter(num=object.card_num2).update(owner_id=object.id)
            if object.status == '0': 
                Card.objects.filter(num=object.card_num1).update(owner_id=None)
                Card.objects.filter(num=object.card_num2).update(owner_id=None)
                messages.warning(self.request,u'已分配卡片将被收回.')
        '''
        if object.cardprt1:
            object.cardprt1.owner_id = object.id
            object.cardprt1.save()
        if object.cardprt2:
            object.cardprt2.owner_id = object.id
            object.cardprt2.save()
        return response 
         
class EmployeeUpdateView(UpdateView):
    form_class= EmployeeForm
    model = Employee
    success_url =  reverse_lazy("employee_list")
    def get_context_data(self, **kwargs):
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.form = form 
        '''
        if self.object.card_num1: 
            form.fields['card_num1'].choices  += [(self.object.card_num1,self.object.card_num1 )]
        if self.object.card_num2:
           form.fields['card_num2'].choices += [(self.object.card_num2,self.object.card_num2 )]
        '''
        context['form'] = form
        context['pageHeader'] = u"员工修改"
        context['title'] = u"员工修改"
        context['sidebar'] = {'employee_list':'active'}
        return context
    '''
    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        form = self.get_form(self.get_form_class()) 
        if self.object.card_num1: 
            form.fields['card_num1'].choices += [(self.object.card_num1,self.object.card_num1 )]
        if self.object.card_num2:
            form.fields['card_num2'].choices += [(self.object.card_num2,self.object.card_num2 )] 
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    '''
    def form_valid(self, form): 
        object = self.get_object()
        logger.info(self.get_object())
        Card.objects.retriveCards(owner_id= object.id, type='5') 
        Card.objects.retriveCards(owner_id= object.id, type='6')
        object = self.object 
        logger.info(self.object)
        if object.status == '0': 
            if object.cardprt1 and object.cardprt2:
                messages.success(self.request, u" %s 已经离职，卡片 %s %s 已被收回！" % (self.object.name, self.object.cardprt1.show_num, self.object.cardprt2.show_num) )
                object.cardprt1 = None
                object.cardprt2 = None
            elif object.cardprt1:
                messages.success(self.request, u" %s 已经离职，卡片 %s 已被收回！" % (self.object.name, self.object.cardprt1.show_num) )
                object.cardprt1 = None
            elif object.cardprt2:
                messages.success(self.request, u" %s 已经离职，卡片 %s 已被收回！" % (self.object.name, self.object.cardprt2.show_num) )
                object.cardprt2 = None
            else:
                messages.success(self.request, u" %s 已经离职!" % (self.object.name) )
           
        else:
            if object.cardprt1:
                object.cardprt1.owner_id = object.id
                object.cardprt1.save()
            if object.cardprt2:
                object.cardprt2.owner_id = object.id
                object.cardprt2.save()
        return super(EmployeeUpdateView, self).form_valid(form)
    def form_invalid(self, form):
        logger.info("invalid %s",  form.is_valid())
        logger.info( u"is bound %s ,  not bool error: %s" , form.is_bound,  not bool(form.errors)) 
        logger.info(u"%s", form.errors) 
        return super(EmployeeUpdateView, self).form_invalid(form)
        
    
class EmployeeDeleteView(DeleteView):
    form_class= EmployeeForm
    model = Employee     
    success_url = reverse_lazy('employee_list') 
    def post(self,request, *args, **kwargs): 
        try:
            object = self.get_object()
            result= super(EmployeeDeleteView, self).post(request, *args, **kwargs)
            if object.cardprt1 and object.cardprt2:
                messages.success(request, u" %s 已被删除，卡片 %s %s 已被收回！" % (object.name, object.cardprt1.show_num, object.cardprt2.show_num) )    
            Card.objects.retriveCards(owner_id= object.id, type='5') 
            Card.objects.retriveCards(owner_id= object.id, type='6')
            return result
        except IntegrityError as e:
            messages.error(request, u" %s 已被使用，不能删除" % self.object.name)
            logger.error(e)
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
    template_name = 'system/materialType_form.html'
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
    template_name = 'system/materialType_form.html'
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
       # cardTypeChoices =  Card.getCardChoices(type="3")
       # logger.info("material card type choices: %s", cardTypeChoices )
       # form.fields['card_num'] = forms.ChoiceField(   choices= [('', '-------')] + cardTypeChoices ,  label="物料卡编号", required=False )
        context['pageHeader'] = u"物料详细信息"
        context['title'] = u"物料详细信息"
        context['sidebar'] = {'material':'active'} 
        return context
    '''
    def post(self, request, **kwargs):
        result = super(MaterialCreateView, self).post(request, **kwargs)
        object = self.object
        if object:
            Card.objects.filter(num=object.card_num).update(owner_id=object.id)
        return result
    '''
    def form_valid(self, form):
        result = super(MaterialCreateView, self).form_valid(form)
        if self.object.cardprt:
            self.object.cardprt.owner_id = self.object.id
            self.object.cardprt.save()
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
        '''
        cardTypeChoices = [('', '-------')]+ Card.getCardChoices(type="3")  
        if self.object.card_num:
            cardTypeChoices += [(self.object.card_num,self.object.card_num ) ]  
        form.fields['card_num'].choices =  cardTypeChoices #forms.ChoiceField(   choices=cardTypeChoices ,  label="物料卡编号", required=False )
        '''
        context['pageHeader'] = u"物料详细信息"
        context['title'] = u"物料详细信息"
        context['sidebar'] = {'material':'active'} 
        return context
    def form_invalid(self, form):
        logger.info(u'%s', form.errors)
        return super(MaterialUpdateView, self).form_invalid(form)
    def form_valid(self, form):
        object = self.object
        Card.objects.retriveCards(type='3', owner_id=self.object.id)
        ''' 
        if self.object.status == '1':
            Card.objects.grantCards(owner_id=self.object.id, num=self.object.card_num)
            if self.object.card_num:
                messages.success(self.request, u" %s 可用，卡片 %s 已下发！" % (self.object.name, self.object.card_num) )
            else:
                messages.success(self.request, u" %s 可用，卡片 %s 已被收回！" % (self.object.name, self.object.card_num) )
        else:
            self.object.card_num = None
            messages.success(self.request, u" %s 已不可用，卡片 %s 已被收回！" % (self.object.name, self.object.card_num) ) 
        return super(MaterialUpdateView, self).form_valid(form)
        '''
        if object.status == '0':
            if object.cardprt:
                messages.success(self.request, u" %s 已不可用，卡片已被收回！" % (self.object.name) )
                card = object.cardprt
                object.cardprt = None
                card.owner_id = 0
                card.save()
        else:
            if object.cardprt:
                object.cardprt.owner_id = object.id
                object.cardprt.save()
        return super(MaterialUpdateView, self).form_valid(form)
    '''
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)  
        cardTypeChoices = [('', '-------')]+ Card.getCardChoices(type="3")  
        if self.object.card_num:
            cardTypeChoices += [(self.object.card_num,self.object.card_num ) ]  
        form.fields['card_num'].choices = cardTypeChoices
        if form.is_valid(): 
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    '''
class MaterialDeleteView(DeleteView):
    form_class= MaterialForm
    model = Material     
    success_url = reverse_lazy('material_list')  
    def post(self,request, *args, **kwargs):
        try:
            object = self.get_object()
            result = super(MaterialDeleteView, self).post(request, *args, **kwargs)
            Card.objects.retriveCards(type='3', owner_id=object.id)
            messages.success(request, u"物料删除成功！") 
            return result
        except IntegrityError as e:
            messages.error(request, u"物料已被使用，不能删除")  
            logger.error(e)
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
    def form_valid(self,form):
        result = super(ProcessCreateView, self).form_valid(form)
        object = self.object
        logger.info(u'%s', self.object)
        if object.cardprt:
            object.cardprt.owner_id = object.id
            object.cardprt.save()
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
        '''
        if self.object.card_num:
            form.fields['card_num'].choices += [(self.object.card_num,self.object.card_num )]
        '''
        return context
    '''
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.get_form_class())
        form.fields['card_num']._set_choices( [('', '------')] + Card.getCardChoices(type='4')) 
        if self.object.card_num: 
            form.fields['card_num'].choices += [(self.object.card_num,self.object.card_num )] 
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    '''    
    def form_valid(self, form):
        object = self.get_object() 
        result = super(ProcessUpdateView, self).form_valid(form)  
        Card.objects.retriveCards(type=4, owner_id=object.id)
        object = self.object
        if object.status == '0':
            if object.cardprt:
                messages.success(self.request, u" %s流程已不可用，卡片 %s 已被收回！" % (self.object.name, self.object.cardprt.show_num) )
                object.cardprt = None
                object.save()
        else:
            if object.cardprt:
                object.cardprt.owner_id = object.id
                object.cardprt.save()
                messages.success(self.request, u"%s流程，新卡片 %s 已被分配！" % (self.object.name, self.object.cardprt.show_num) )
            else:
                messages.warning(self.request, u"%s流程，未分配卡片！" % (self.object.name) )
        return result
    def form_invalid(self, form):
        #logger.info(form.is_valid())
        logger.info(u'%s', form.errors)
        return super(ProcessUpdateView, self).form_invalid(form)
        
    
class ProcessDeleteView(DeleteView):
    form_class= ProcessForm
    model = Process     
    success_url = reverse_lazy('process_list')  
    def post(self,request, *args, **kwargs):
        try:
            object = self.get_object()
            result = super(ProcessDeleteView, self).post(request, *args, **kwargs) 
            Card.objects.retriveCards(type=4, owner_id=object.id)
            messages.success(request, u"工艺已被成功删除！")  
            return result
        except IntegrityError as e:
            messages.error(request, u"工艺已被使用，不能删除！") 
            logger.error(e)
        return redirect('process_list');
    def get_context_data(self, **kwargs):
        context = super(ProcessDeleteView, self).get_context_data(**kwargs) 
        context['sidebar'] = {'process':'active'} 
        return context
#--------------------------------------------------班次管理 界面定义------------------------------------------------------------------   
from system.models import WorkClass, WorkClassForm, NormalSearchForm

class WorkClassListView(SystemListView): 
    template_name = 'system/workclass_list.html'
    context_object_name = 'workclass_list'
    model = WorkClass
    form_class = NormalSearchForm
    #paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super(WorkClassListView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"班次管理"
        context['title'] = u"班次管理" 
        context['sidebar'] = {'workclass':'active'} 
        context['add_url'] = reverse_lazy("workclass_add")
        return context  

class WorkClassDetailView(SystemDetailView): 
    template_name = 'system/workclass_detail.html'
    context_object_name = 'workclass'
    model = WorkClass
    def get_context_data(self, **kwargs): 
        context = super(WorkClassDetailView, self).get_context_data(**kwargs)  
        context['pageHeader'] = u"班次详细信息"
        context['title'] = u"班次详细信息"
        context['sidebar'] = {'workclass':'active'}   
        return context

class WorkClassCreateView(CreateView):
    form_class= WorkClassForm
    model = WorkClass
    def get_context_data(self, **kwargs):
        context = super(WorkClassCreateView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class) 
        context['form'] = form
        #form.fields['card_num'].choices =   [('', '------')] + Card.getCardChoices(type=1) + Card.getCardChoices(type=2) 
        context['pageHeader'] = u"创建班次信息"
        context['title'] = u"创建班次信息"
        context['sidebar'] = {'workclass':'active'}   
        return context
    def form_valid(self, form):
        response = super(WorkClassCreateView, self).form_valid(form) 
        object = self.object
        if object.cardprt:
            object.cardprt.owner_id = object.id
            object.cardprt.save()
        #logger.info(object.card_num)
        #Card.objects.filter(num=object.card_num).update(owner_id=object.id)
        return response
    success_url =  reverse_lazy("workclass_list")
        
class WorkClassUpdateView(UpdateView):
    form_class= WorkClassForm
    model = WorkClass
    success_url =  reverse_lazy("workclass_list")
    def form_valid(self, form):
        object = self.get_object() 
        result = super(WorkClassUpdateView, self).form_valid(form)  
        Card.objects.retriveCards(type=1, owner_id=object.id)
        Card.objects.retriveCards(type=2, owner_id=object.id)
        object = self.object
        if object.status == '0':
            if object.cardprt:
                messages.success(self.request, u" %s班次已不可用，卡片 %s 已被收回！" % (self.object.name, self.object.cardprt.show_num) )
                card = object.cardprt
                object.cardprt = None
                card.owner_id = 0
                card.save()
                object.save()
        else:
            if object.cardprt:
                object.cardprt.owner_id = object.id
                object.cardprt.save()
                messages.success(self.request, u"%s班次，新卡片 %s 已被分配！" % (self.object.name, self.object.cardprt.show_num) )
            else:
                messages.warning(self.request, u"%s班次，未分配卡片！" % (self.object.name) )
        return result
    
    
class WorkClassDeleteView(DeleteView):
    form_class= WorkClassForm
    model = WorkClass
    success_url = reverse_lazy("workclass_list")
    def post(self,request, *args, **kwargs):
        try:
            object = self.get_object()
            result = super(WorkClassDeleteView, self).post(request, *args, **kwargs)
            Card.objects.retriveCards(type='1', owner_id=object.id)
            Card.objects.retriveCards(type='2', owner_id=object.id)
            messages.success(request, u"班次删除成功！") 
            return result
        except IntegrityError as e:
            messages.error(request, u"班次已被使用，不能删除")  
            logger.error(e)
            return redirect('workclass_list');
    def get_context_data(self, **kwargs):
        context = super(WorkClassDeleteView, self).get_context_data(**kwargs)
        context['sidebar'] = {'workclass':'active'} 
        return context
    



 
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
    success_url = reverse_lazy('salarycount_list')
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
    success_url = reverse_lazy('salarytime_list')
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
        context['pageHeader'] = u"卡管理"
        context['title'] = u"卡管理"
        context['sidebar'] = {'card':'active'}
        context['add_url'] = reverse_lazy('card_add')
        context['is_display'] = 'none'
       # context['form'] = self.get_form_class()(cache.get('card_queryDict'))
        logger.info(context['page_obj'] )
        #cache.set('card_page', context['page_obj'] , 15 * 60)
        return context
   
    def get_queryset(self):
        q = self.get_query_string()
        logger.info(q)  
        #if len(q):
        #    cache.set('card_queryDict', q , 15 * 60)
        #else: 
        #    q = cache.get('card_queryDict')
        return Card.objects.searchCards(q)
    def get_success_url(self):
        logger.info(cache.get('card_page').number)
        return reverse_lazy('card_list', kwargs={'page': cache.get('card_page').number})  
        
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
        #logger.info("card form: %s", form_class)
        #logger.info(self.get_object())
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
    def form_valid(self, form): 
        response = super(CardUpdateView, self).form_valid(form)
        card = self.object
        if card.status == '0':
            if card.type == '4' and card.owner_id <> 0 :
                process = card.process
                process.cardprt = None
                process.save()                
            if card.type == '3' and card.owner_id <> 0:
                material = card.material
                material.cardprt = None
                material.save()
            if card.type == '6' and card.owner_id <> 0:
                employee = card.work_card
                employee.cardprt2 = None
                employee.save()
            if card.type=='5' and card.owner_id <> 0:
                employee = card.employ_card
                employee.cardprt1 = None
                employee.save()
            if (card.type == '1' or card.type == '2') and card.owner_id <> 0:
                workclass = card.workclass
                workclass.cardprt = None
                workclass.save() 
            card.owner_id = 0
            card.save()
        return response
    '''
    def update_card_owner(self):
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
            logger.info("owner: %s", owner)
            owner.save()
        if owner_id:
            logger.info("card type %s owner_id:%s", card.type, owner_id)
            owner = owner_getter.get(card.type).get(pk = owner_id)
            logger.info("owner: %s", owner)
            if card.type == '5':
                owner.card_num1 = ''
            elif card.type == '6':
                owner.card_num2 = ''
            else:
                logger.info("set owner card_num to None")
                owner.card_num = ''
            owner.save()
    '''    
    def render_to_json_response(self, context, **response_kwargs):
        logger.info(self.get_object().__dict__)
        data = self.get_object().__dict__
        del data['_state'] 
        data = json.dumps(data)
        logger.info(data)
        #response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, content_type='application/json')
        #def get_form(self,form_class):  不需要编辑拥有着功能因此注释掉 2014.06.04 /shanhu
     #   form = super(CardUpdateView, self).get_form(form_class)
      #  logger.info(" object: %s", self.get_object() )        
      #  logger.info( u"form running times: %s   type : %s ", form, self.get_object().type ) 
    #    form = self.update_type_field(form)
      #  logger.info("%s", form)
    #    return form
   
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
        obj = self.get_object()
        materials = [(0, '---------')] + [(material.id, material.name) for material in Material.objects.filter(Q(card_num__isnull=True) | Q(card_num='') )]
        if obj.owner_id <> 0l:
            materials += [(material.id, material.name) for material in  Material.objects.filter(pk=obj.owner_id)]
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
from system.models import Production, ProductionSearchForm, ReportEmployee, ReportEmployeeSearchForm,  ReportClass, ReportClassSearchForm
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
        context['is_display'] = 'none'
        context['sidebar'] = {'data_live':'active'} 
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
            select pd.id ID, e.NUM EMPLOYEE_NUM,e.NAME EMPLOYEE_NAME ,m.NAME MATERIAL_NAME ,if(ps.IS_FIRST,'领料','交料') IS_FIRST,  ps.name PROCESS_NAME ,pd.COUNT START_COUNT ,pd.TIME START_TIME 
            from production pd
            join process ps on pd.PROCESS_ID = ps.ID
            join material m on m.id = pd.MATERIAL_ID
            join employee e on e.ID = pd.EMPLOYEE_ID 
            WHERE 1=1
            
        '''
        if "start_time" in self.request.GET and "end_time" in self.request.GET:
            start_time = self.request.GET['start_time']
            end_time = self.request.GET['end_time']
            if start_time and end_time:
                 querySql += " and ( pd.TIME between '%s' and '%s')   " % (start_time, end_time + ' 23:59:59'  )
        else:
            querySql += " and ( pd.TIME between '%s' and '%s')   " % (datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d') + ' 23:59:59'  )
                
        if "is_first" in self.request.GET:
            is_first =  self.request.GET['is_first']
            if is_first:
                querySql += "and ps.is_first = %s " % is_first
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
        logger.info(querySql   + "  order by   pd.time desc, pd.EMPLOYEE_ID ,pd.MATERIAL_ID ")
        return list(Production.objects.raw(querySql   + "  order by   pd.time desc, pd.EMPLOYEE_ID ,pd.MATERIAL_ID "))
class ReportEmployeeListView(SystemListView):
    template_name = 'system/reportemployee_list.html'
    context_object_name = 'reportemployee_list'
    model = ReportEmployee
    form_class = ReportEmployeeSearchForm
    #paginate_by = 10
    #logger.info("system out test.") 
    def get_context_data(self, *args, **kwargs):
        context = super(ReportEmployeeListView, self).get_context_data(*args, **kwargs)
        context['pageHeader'] = u"员工汇总"
        context['title'] = u"数据中心"
        context['is_display'] = 'none'
        context['sidebar'] = {'report_employee':'active'} 
        return context
    def get_queryset(self):
        querySql = '''
         SELECT RP.ID, E.name EMPLOYEE_NAME,WS.NAME WORKSHOP_NAME,M.NAME MATERIAL_NAME,BPS.NAME FIRST_PROCESS_NAME,APS.NAME LAST_PROCESS_NAME,SUM(RP.PUT_COUNT) PUT_COUNT, SUM(RP.GET_COUNT) GET_COUNT ,  ROUND(SUM(RP.PUT_COUNT) /  SUM(RP.GET_COUNT) * 100 ,2) AVERAGERATE 
            FROM REPORT_EMPLOYEE RP 
            LEFT JOIN WORKSHOP WS ON WS.ID = RP.WORKSHOP_ID
            LEFT JOIN MATERIAL M ON M.ID = RP.MATERIAL_ID
            LEFT JOIN PROCESS BPS ON BPS.ID = RP.PROCESS_FIRST_ID
            LEFT JOIN PROCESS APS ON APS.ID = RP.PROCESS_LAST_ID
		    left join employee e on e.id = RP.employee_id
            WHERE 1=1
         '''
        if "start_time" in self.request.GET and "end_time" in self.request.GET:
            start_time = self.request.GET['start_time']
            end_time = self.request.GET['end_time']
            if start_time and end_time:
                 querySql += "and ( RP.STARTTIME between '%s' and '%s' or RP.ENDTIME between '%s' and '%s'  )   " % (start_time, end_time + ' 23:59:59' , start_time, end_time + ' 23:59:59' )

        if "process" in self.request.GET:
            process = self.request.GET['process']
            if process:
                querySql += "and ( RP.PROCESS_FIRST_ID = '%s' or RP.PROCESS_LAST_ID = '%s'   )   " % (process, process )
        if "employee_num" in self.request.GET:
            employee_num =  self.request.GET['employee_num']
            if employee_num:
                querySql += "and e.NUM = %s " % employee_num
        if "employee_name" in self.request.GET:
            employee_name =  self.request.GET['employee_name']
            if employee_name:
                querySql += "and e.NAME = '%s' " % employee_name
        if "material" in self.request.GET:
            material = self.request.GET['material']
            if material:
                querySql += "and RP.MATERIAL_ID = '%s' " % material
        return list(Production.objects.raw(querySql   + "  group by RP.employee_id, rp.WORKSHOP_ID,rp.MATERIAL_ID,rp.PROCESS_FIRST_ID,rp.PROCESS_LAST_ID "))
class ReportEmployeeDetailListView(SystemListView):
    template_name = 'system/reportemployeedetail_list.html'
    context_object_name = 'reportemployee_list'
    model = ReportEmployee
    form_class = ReportEmployeeSearchForm
    #paginate_by = 10
    #logger.info("system out test.") 
    def get_context_data(self, *args, **kwargs):
        context = super(ReportEmployeeDetailListView, self).get_context_data(*args, **kwargs)
        context['pageHeader'] = u"员工汇总明细"
        context['title'] = u"数据中心"
        context['is_display'] = 'none'
        context['sidebar'] = {'report_employee_detail':'active'} 
        return context
    def get_queryset(self):
        querySql = '''
         SELECT RP.ID, E.name EMPLOYEE_NAME,WS.NAME WORKSHOP_NAME,M.NAME MATERIAL_NAME,BPS.NAME FIRST_PROCESS_NAME,APS.NAME LAST_PROCESS_NAME,RP.PUT_COUNT PUT_COUNT, RP.GET_COUNT GET_COUNT ,  RP.AVERAGE_RATE AVERAGERATE ,RP.STARTTIME STARTTIME, RP.ENDTIME ENDTIME
            FROM REPORT_EMPLOYEE RP 
            LEFT JOIN WORKSHOP WS ON WS.ID = RP.WORKSHOP_ID
            LEFT JOIN MATERIAL M ON M.ID = RP.MATERIAL_ID
            LEFT JOIN PROCESS BPS ON BPS.ID = RP.PROCESS_FIRST_ID
            LEFT JOIN PROCESS APS ON APS.ID = RP.PROCESS_LAST_ID
		    left join employee e on e.id = RP.employee_id
            WHERE 1=1
         '''
        if "start_time" in self.request.GET and "end_time" in self.request.GET:
            start_time = self.request.GET['start_time']
            end_time = self.request.GET['end_time']
            if start_time and end_time:
                 querySql += "and ( RP.STARTTIME between '%s' and '%s' or RP.ENDTIME between '%s' and '%s'  )   " % (start_time, end_time + ' 23:59:59' , start_time, end_time + ' 23:59:59' )

        if "process" in self.request.GET:
            process = self.request.GET['process']
            if process:
                querySql += "and ( RP.PROCESS_FIRST_ID = '%s' or RP.PROCESS_LAST_ID = '%s'   )   " % (process, process )
        if "employee_num" in self.request.GET:
            employee_num =  self.request.GET['employee_num']
            if employee_num:
                querySql += "and e.NUM = %s " % employee_num
        if "employee_name" in self.request.GET:
            employee_name =  self.request.GET['employee_name']
            if employee_name:
                querySql += "and e.NAME = '%s' " % employee_name
        if "material" in self.request.GET:
            material = self.request.GET['material']
            if material:
                querySql += "and RP.MATERIAL_ID = '%s' " % material
        return list(Production.objects.raw(querySql))

class ReportClassListView(SystemListView):
    template_name = 'system/reportclass_list.html'
    context_object_name = 'reportclass_list'
    model = ReportClass
    form_class = ReportClassSearchForm
    #paginate_by = 10
    #logger.info("system out test.") 
    def get_context_data(self, *args, **kwargs):
        context = super(ReportClassListView, self).get_context_data(*args, **kwargs)
        context['pageHeader'] = u"班次汇总"
        context['title'] = u"数据中心"
        context['sidebar'] = {'report_class':'active'} 
        context['is_display'] = 'none'
        return context
    def get_queryset(self):
        querySql = '''
         SELECT RP.ID,WS.NAME WORKSHOP_NAME,M.NAME MATERIAL_NAME,BPS.NAME FIRST_PROCESS_NAME,APS.NAME LAST_PROCESS_NAME,SUM(RP.PUT_COUNT) PUT_COUNT, SUM(RP.GET_COUNT) GET_COUNT ,  ROUND(SUM(RP.PUT_COUNT) /  SUM(RP.GET_COUNT) * 100 ,2) AVERAGERATE 
            FROM REPORT_CLASS RP 
            LEFT JOIN WORKSHOP WS ON WS.ID = RP.WORKSHOP_ID
            LEFT JOIN MATERIAL M ON M.ID = RP.MATERIAL_ID
            LEFT JOIN PROCESS BPS ON BPS.ID = RP.PROCESS_FIRST_ID
            LEFT JOIN PROCESS APS ON APS.ID = RP.PROCESS_LAST_ID
            WHERE 1=1
         '''
     
        if "start_time" in self.request.GET and "end_time" in self.request.GET:
            start_time = self.request.GET['start_time']
            end_time = self.request.GET['end_time']
            if start_time and end_time:
                querySql += "and ( RP.STARTTIME between '%s' and '%s' or RP.ENDTIME between '%s' and '%s'  )   " % (start_time, end_time + ' 23:59:59' , start_time, end_time + ' 23:59:59' )
        if "process" in self.request.GET:
            process = self.request.GET['process']
            if process:
                querySql += "and ( RP.PROCESS_FIRST_ID = '%s' or RP.PROCESS_LAST_ID = '%s'   )   " % (process, process )
        if "material" in self.request.GET:
            material = self.request.GET['material']
            if material:
                querySql += "and RP.MATERIAL_ID = '%s' " % material
        return list(Production.objects.raw(querySql   + "  GROUP BY RP.WORKSHOP_ID,RP.MATERIAL_ID,RP.PROCESS_FIRST_ID,RP.PROCESS_LAST_ID "))
         
class ReportClassDetailListView(SystemListView):
    template_name = 'system/reportclassdetail_list.html'
    context_object_name = 'reportclass_list'
    model = ReportClass
    form_class = ReportClassSearchForm
    #paginate_by = 10
    #logger.info("system out test.") 
    def get_context_data(self, *args, **kwargs):
        context = super(ReportClassDetailListView, self).get_context_data(*args, **kwargs)
        context['pageHeader'] = u"班次汇总明细"
        context['title'] = u"数据中心"
        context['sidebar'] = {'report_class_detail':'active'} 
        context['is_display'] = 'none'
        return context
    def get_queryset(self):
        querySql = '''
         SELECT RP.ID,WS.NAME WORKSHOP_NAME,M.NAME MATERIAL_NAME,BPS.NAME FIRST_PROCESS_NAME,APS.NAME LAST_PROCESS_NAME, RP.PUT_COUNT PUT_COUNT, RP.GET_COUNT GET_COUNT ,  RP.AVERAGE_RATE AVERAGERATE ,RP.STARTTIME STARTTIME, RP.ENDTIME ENDTIME
            FROM REPORT_CLASS RP 
            LEFT JOIN WORKSHOP WS ON WS.ID = RP.WORKSHOP_ID
            LEFT JOIN MATERIAL M ON M.ID = RP.MATERIAL_ID
            LEFT JOIN PROCESS BPS ON BPS.ID = RP.PROCESS_FIRST_ID
            LEFT JOIN PROCESS APS ON APS.ID = RP.PROCESS_LAST_ID
            WHERE 1=1
         '''
     
        if "start_time" in self.request.GET and "end_time" in self.request.GET:
            start_time = self.request.GET['start_time']
            end_time = self.request.GET['end_time']
            if start_time and end_time:
                querySql += "and ( RP.STARTTIME between '%s' and '%s' or RP.ENDTIME between '%s' and '%s'  )   " % (start_time, end_time + ' 23:59:59' , start_time, end_time + ' 23:59:59' )
        if "process" in self.request.GET:
            process = self.request.GET['process']
            if process:
                querySql += "and ( RP.PROCESS_FIRST_ID = '%s' or RP.PROCESS_LAST_ID = '%s'   )   " % (process, process )
        if "material" in self.request.GET:
            material = self.request.GET['material']
            if material:
                querySql += "and RP.MATERIAL_ID = '%s' " % material
        return list(Production.objects.raw(querySql))

from system.models import Terminal, TerminalForm
class TerminalListView(SystemListView):
    template_name = 'system/terminal_list.html'
    context_object_name = 'terminal_list'
    model = Terminal
    form_class = TerminalForm
    def get_context_data(self, *args, **kwargs):
        context = super(TerminalListView, self).get_context_data(*args, **kwargs)
        context['pageHeader'] = u"终端管理"
        context['title'] = u"数据中心"
        context['sidebar'] = {'terminal_list':'active'} 
        context['is_display'] = 'none'
        return context
    def get_queryset(self):
         querySql = '''
         select t.id ID ,t.num TNUM ,t.name TNAME , dc.TYPE_DESC TTYPEDESC,wg.name  WGNAME ,ws.name WSNAME ,dm.NAME DMNAME ,dp.name DPNAME ,cp.name CPNAME,cm.name CMNAME
            from terminal t
            left join workgroup wg on wg.ID = t.WORKGROUP_ID
            left join workshop ws on ws.id = wg.WORKSHOP_ID
            left join material dm on dm.ID = t.DEFAULT_MATERIAL_ID
            left join process dp  on dp.ID = t.DEFAULT_PROCESS_ID
            left join material cm on cm.id  = t.CURRENT_MATERIAL_ID
            left join process cp  on cp.ID = t.CURRENT_PROCESS_ID
            left join dictionary_config dc on dc.TYPE = 'terminal_type' and dc.type_code = t.type
            where 1 = 1 
         '''
         if "workshop" in self.request.GET:
            workshop = self.request.GET['workshop']
            if workshop:
                querySql += " and ws.id = %s " % (workshop)
         return list(Terminal.objects.raw(querySql))
from system.models import Workshop 
class WorkshopListView(SystemListView):
    template_name = 'system/workshop_list.html'
    context_object_name = 'workshop_list'
    model = Workshop 
    def get_context_data(self, *args, **kwargs):
        context = super(WorkshopListView, self).get_context_data(*args, **kwargs)
        context['pageHeader'] = u"车间管理"
        context['title'] = u"数据中心"
        context['sidebar'] = {'workshop_list':'active'} 
        context['is_display'] = 'none'
        return context
    def get_queryset(self):
         querySql = '''
         SELECT RP.ID,WS.NAME WORKSHOP_NAME,M.NAME MATERIAL_NAME,BPS.NAME FIRST_PROCESS_NAME,APS.NAME LAST_PROCESS_NAME, RP.PUT_COUNT PUT_COUNT, RP.GET_COUNT GET_COUNT ,  RP.AVERAGE_RATE AVERAGERATE ,RP.STARTTIME STARTTIME, RP.ENDTIME ENDTIME
            FROM REPORT_CLASS RP 
            LEFT JOIN WORKSHOP WS ON WS.ID = RP.WORKSHOP_ID
            LEFT JOIN MATERIAL M ON M.ID = RP.MATERIAL_ID
            LEFT JOIN PROCESS BPS ON BPS.ID = RP.PROCESS_FIRST_ID
            LEFT JOIN PROCESS APS ON APS.ID = RP.PROCESS_LAST_ID
            WHERE 1=1
         '''
         return list(Workshop.objects.raw(querySql))
