# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
       
class DictConfig(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.    
    typeCode = models.CharField(db_column='TYPE_CODE', max_length=20, blank=True) # Field name made lowercase.    
    typeDesc = models.CharField(db_column='TYPE_DESC', max_length=50, blank=True) # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=20, blank=True) # Field name made lowercase.
    dicTable = models.CharField(db_column='DIC_TABLE', max_length=30, blank=True) # Field name made lowercase.
    dicColumn = models.CharField(db_column='DIC_COLUMN', max_length=30, blank=True) # Field name made lowercase.    
    displayOrder = models.IntegerField(db_column='DISPLAY_ORDER',  blank=True) # Field name made lowercase.
    class Meta:
       # managed = False
       db_table = 'dictionary_config'
    def __unicode__(self):  # Python 3: def __str__(self):
            return  u"id {0} num {1} name {2}   remarks {3} ".format(self.id , self.typeCode ,  self.typeDesc ,  self.type)
    @staticmethod
    def getTypeChoices(**kwargs):
       # types = DictConfig.objects.filter(**kwargs).order_by("displayOrder")
        choices = [(type.typeCode, type.typeDesc) for type in DictConfig.objects.filter(**kwargs).order_by("displayOrder")] 
        # []
     #   for t in types:
       #     choices.append((t.typeCode, t.typeDesc)) 
        return choices 

class Card(models.Model):
    cardTypeChoices = DictConfig.getTypeChoices(type="card_type")
    cardStatusChoices = DictConfig.getTypeChoices(type="card_status")
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20 , verbose_name="卡号", editable = False) # Field name made lowercase.
    serial_num = models.CharField(db_column='SERIAL_NUM' , max_length=20,   editable = False ) # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, choices=cardTypeChoices , editable = False,  verbose_name="卡类型") # Field name made lowercase.
    owner_id = models.IntegerField(db_column='OWNER_ID', blank=True, null=True, verbose_name="所有者") # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1 , choices=cardStatusChoices, verbose_name="状态") # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200 , editable = False, blank=True, verbose_name="备注") # Field name made lowercase.
    class Meta:
        #managed = False
        db_table = 'card'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} type {2} owner_id {4} remarks {3} ".format(self.id , self.num , self.type,  self.remarks, self.owner_id)
    @staticmethod
    def getTypeChoices(**kwargs):
        return   [('', '--------')] + [(card.id, card.num) for card in Card.objects.filter(**kwargs)] 


class CardForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs) 
    class Meta:
        model = Card  
        fields = '__all__'
      
        

class CardSearchForm(forms.Form):
    typeChoices = DictConfig.getTypeChoices(type="card_type") 
    assignedChoices = DictConfig.getTypeChoices(type="card_assigned") 
    num = forms.CharField(max_length=20, label= u"", widget=forms.TextInput(attrs={'placeholder':'卡号'}), required = False )
    type = forms.CharField(max_length=1, widget=forms.Select(choices= [('', '全部')] + typeChoices, attrs={'placeholder':'卡号'}) , label= u"", required = False) # Field name made lowercase.   e 
    assignd = forms.CharField(max_length=1, label = "",  widget=forms.Select( choices= [('', '全部')] + assignedChoices), required = False)
        
    
        
class Employee(models.Model):
    
    sexChoices = DictConfig.getTypeChoices(type="sex")
    employeeTypeChoices  = DictConfig.getTypeChoices(type="employee_type")
    statusChoices = DictConfig.getTypeChoices(type="employee_status")
    
   # employeeCardChoices = Card.objects.filter()
    
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, verbose_name="员工号",  unique=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, verbose_name="姓名") # Field name made lowercase.
    sex = models.CharField(db_column='SEX', max_length=1, verbose_name="性别" , choices=sexChoices  ) # Field name made lowercase.
    idCard = models.CharField(db_column='IDCARD', max_length=20,verbose_name="身份证") # Field name made lowercase.
    tel = models.CharField(db_column='TEL', max_length=20, blank=True,  verbose_name="联系方式") # Field name made lowercase.
    joinTime = models.DateTimeField(db_column='JOIN_TIME' , )#verbose_name="入职时间"
    type = models.CharField(db_column='TYPE', max_length=1, verbose_name="员工类型",  choices=employeeTypeChoices) # Field name made lowercase.   
    status = models.CharField(db_column='STATUS', max_length=1, verbose_name="员工状态" , choices=statusChoices) # Field name made lowercase.
    card_num1 = models.CharField(db_column='CARD_NUM1', max_length=20,  null=True, blank=True,verbose_name="工作卡号",    ) # Field name made lowercase.
    card_num2 = models.CharField(db_column='CARD_NUM2', max_length=20,  null=True, blank=True,verbose_name="员工卡号",    ) # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True,verbose_name="备注") # Field name made lowercase.
     
    class Meta:
       # managed = False
        db_table = 'employee'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2} card_num1{4},card_num2{5} remarks {3} ".format(self.id , self.num ,  self.name ,  self.remarks, self.card_num1, self.card_num2)
    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={'pk': self.pk})


        

class Workshop(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True) # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase.
    class Meta:
     #   managed = False
        db_table = 'workshop'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} name {1}  ".format(self.id ,  self.name )

class WorkGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True) # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase.
    workshop = models.ForeignKey(Workshop, db_column='WORKSHOP_ID', blank=True, null=True) # Field name made lowercase.
    class Meta:
     #   managed = False
        db_table = 'work_group'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} name {1}  ".format(self.id ,  self.name ) 
  

class MaterialType(models.Model):
    choices = DictConfig.getTypeChoices(type = 'material_type_status')
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20,   unique=True , verbose_name="编号") # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20  , verbose_name="名称") # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, verbose_name="状态", choices=choices) # Field name made lowercase.
    parent = models.ForeignKey('self', db_column='PARENT_ID', blank=True, null=True, verbose_name="父类型") # Field name made lowercase.
    class Meta:
     #   managed = False
        db_table = 'material_type'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u" {0} ".format(self.num, )
        
class MaterialTypeForm(forms.ModelForm): 
    statusChoices =  DictConfig.getTypeChoices(type="material_type_status")
    class Meta:
        model = MaterialType
        fields  = ['num', 'status', 'parent',   ]   
    status = forms.CharField( max_length=1, widget=forms.Select(choices=statusChoices) , label="物料类型状态" ) # Field name made lowercase.                



class Material(models.Model):
    statuschoices = DictConfig.getTypeChoices(type = 'material_status')
    
    
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20 , unique=True, verbose_name="编号") # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, verbose_name="名称") # Field name made lowercase.
    materialType = models.ForeignKey(MaterialType, db_column='MATERIAL_TYPE_ID', blank=True, null=True, verbose_name="类型") # Field name made lowercase.
    
  
   # conver = models.IntegerField(db_column='CONVER', blank=True, null=True,  verbose_name="换算") # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True , choices=statuschoices) # Field name made lowercase.
    card_num = models.CharField(db_column='CARD_NUM', max_length=20, blank=True,   null=True, verbose_name="物料卡编号") # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True, verbose_name="备注") # Field name made lowercase.
    class Meta:
       # managed = False
        db_table = 'material'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u" 编号({0}) 名称({1}) 物料卡号({2})".format(  self.num ,  self.name  , self.card_num )

   
class MaterialForm(forms.ModelForm): 
    statusChoices =  DictConfig.getTypeChoices(type="material_status")
    modeChoices =  DictConfig.getTypeChoices(type="material_mode")
    class Meta:
        model = Material
        fields  = '__all__'
    status = forms.CharField( max_length=1, widget=forms.Select(choices=statusChoices) , label="物料状态" ) # Field name made lowercase. 
    mode = forms.CharField( max_length=1, widget=forms.Select(choices=modeChoices) , label="统计方式" ) # Field name made lowercase.                


 
class Process(models.Model):
    processIsFirstchoices = DictConfig.getTypeChoices(type = 'process_isfirst')
    statuschoices = DictConfig.getTypeChoices(type = 'process_status')
    modechoices = DictConfig.getTypeChoices(type = 'material_mode')
    
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, unique=True, verbose_name="编号") # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, verbose_name="名称") # Field name made lowercase.
    firstProcess = models.ForeignKey('self', db_column='FIRST_PROCESS_ID', blank=True, null=True, verbose_name="前工艺") # Field name made lowercase.
    isFirst = models.CharField(db_column='IS_FIRST', max_length=1, choices=processIsFirstchoices, verbose_name="是否前工艺"  ) # Field name made lowercase.    
    status = models.CharField(db_column='STATUS', max_length=1, choices=statuschoices, verbose_name="状态") # Field name made lowercase.
    card_num = models.CharField(db_column='CARD_NUM', max_length=20, blank=True, null=False, verbose_name="工艺卡号") # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True, verbose_name="备注") # Field name made lowercase.
    mode = models.CharField(db_column='MODE', max_length=1, blank=True ,  verbose_name="统计方式", choices=modechoices) # Field name made lowercase
    unit = models.CharField(db_column='UNIT', max_length=20, blank=True ,  verbose_name="单位") # Field name made lowercase..
    class Meta:
       # managed = False
        db_table = 'process'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u" 编号({0})  名称({1})  工艺卡号({2})".format( self.num ,  self.name ,   self.card_num)

class ProcessForm(forms.ModelForm):  
    class Meta:
        model = Process
        fields  = '__all__' 

         
class Terminal(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, blank=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True) # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, blank=True) # Field name made lowercase.
    workGroup = models.ForeignKey(WorkGroup, db_column='WORKGROUP_ID', blank=True, null=True) # Field name made lowercase.
    ip1 = models.CharField(db_column='IP1', max_length=20, blank=True) # Field name made lowercase.
    ip2 = models.CharField(db_column='IP2', max_length=20, blank=True) # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase.
    defaultMaterial = models.ForeignKey(Material, db_column='DEFAULT_MATERIAL_ID', blank=True, null=True) # Field name made lowercase.
    defaultProcess = models.ForeignKey(Process, db_column='DEFAULT_PROCESS_ID', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'terminal'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2}   remarks {3} ".format(self.id , self.num ,  self.name ,  self.remarks)
        

class Workshift(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    terminal = models.ForeignKey(Terminal, db_column='TERMINAL_ID') # Field name made lowercase.
    card = models.ForeignKey(Card, db_column='CARD_ID') # Field name made lowercase.
    time = models.DateTimeField(db_column='TIME') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'workshift'  

class EmployeeForm(forms.ModelForm):
    #sexChoices = DictConfig.getTypeChoices(type="sex") 
    employeeTypeChoices  = DictConfig.getTypeChoices(type="employee_type")
    statusChoices = DictConfig.getTypeChoices(type="employee_status")
    joinTime = forms.DateTimeField( required=False,widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm","pickSeconds": False}),label="入职时间" )
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['sex'] = forms.ChoiceField(choices=DictConfig.getTypeChoices(type='sex'), label="性别", )
       #TODO self.fields['card_num1'] = forms.ChoiceField(choices=)
    class Meta:
        model = Employee
        fields  = ['num', 'name', 'idCard','sex', 'tel','joinTime' , 'type', 'status', 'card_num1', 'card_num2', 'remarks',   ]
    #sex = forms.CharField(max_length=1 ,  label="性别") # Field name made lowercase.    
    type = forms.CharField(max_length=1, widget=forms.Select(choices=employeeTypeChoices) , label="员工类型", ) # Field name made lowercase.   
    status = forms.CharField( max_length=1, widget=forms.Select(choices=statusChoices) , label="员工状态" ) # Field name made lowercase.    
    
        
    input_formats = ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
        '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
        '%Y-%m-%d',              # '2006-10-25'
        ]
   # joinTime = forms.DateTimeField(input_formats=input_formats, widget=widgets.SelectDateWidget(),  label="入职时间", )
class EmployeeSearchForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'num']
        labels = {'name':'','num':''}
        widgets = {'name':forms.TextInput(attrs={'placeholder':'姓名'}),
                   'num':forms.TextInput(attrs={'placeholder':'编号'})}
    
    
    


class WorkClass(models.Model):    
    clasTypeChoices = DictConfig.getTypeChoices(type="class_type")
    classStatusTypeChoices  = DictConfig.getTypeChoices(type="class_status")    
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, unique=True, verbose_name="编号",) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True, verbose_name="名称",) # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, blank=True, verbose_name="类型",  choices=clasTypeChoices) # Field name made lowercase.   
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, verbose_name="状态", choices=classStatusTypeChoices) # Field name made lowercase.
    card_num = models.CharField(db_column='CARD_NUM', max_length=20,  null=True, verbose_name="班次卡号", blank=True) # Field name made lowercase. 
    remarks = models.TextField(db_column='REMARKS', max_length=200, verbose_name="备注", blank=True) # Field name made lowercase.     
    class Meta:
       # managed = False
        db_table = 'work_class'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2}   remarks {3} ".format(self.id , self.num ,  self.name ,  self.remarks)


class WorkClassForm(forms.ModelForm):  
    class Meta:
        model = WorkClass
        fields  = '__all__'
 


class Attendance(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    terminal = models.ForeignKey('Terminal', db_column='TERMINAL_ID') # Field name made lowercase.
    employee = models.ForeignKey('Employee', db_column='EMPLOYEE_ID') # Field name made lowercase.
    card = models.ForeignKey('Card', db_column='CARD_ID') # Field name made lowercase.
    time = models.DateTimeField(db_column='TIME') # Field name made lowercase.
    class Meta:
        #managed = False
        db_table = 'attendance'

  

class SalaryCountConfig(models.Model): 
    iddefaultsChoices = DictConfig.getTypeChoices(type="salary_count_default")
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    material = models.ForeignKey(Material, db_column='MATERIAL_ID',verbose_name="物料" ,  ) # Field name made lowercase.
    process = models.ForeignKey(Process, db_column='PROCESS_ID',verbose_name="工艺" ,  ) # Field name made lowercase.
    price = models.DecimalField(db_column='PRICE', max_digits=10, decimal_places=2,verbose_name="单价" ) # Field name made lowercase.
   # isDefault = models.CharField(db_column='IS_DEFAULT', max_length=1, blank=True,verbose_name="是否默认", choices=iddefaultsChoices ) # Field name made lowercase.
   # startTime = models.DateTimeField(db_column='START_TIME',  blank=True,verbose_name="开始时间"  ) # Field name made lowercase.
   # endTime = models.DateTimeField( db_column='END_TIME',  blank=True,verbose_name="结束时间" ) # Field name made lowercase. 
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True,verbose_name="备注" ) # Field name made lowercase. 
    class Meta:
       # managed = False
        db_table = 'salary_count_config'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2}   remarks {3} ".format(self.id , self.price ,  self.isDefault ,  self.remarks)
 

class SalaryCountConfigForm(forms.ModelForm): 
   # startTime = forms.DateTimeField( required=False,widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm","pickSeconds": False}),label="开始时间" )
  #  endTime =  forms.DateTimeField( required=False,widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm","pickSeconds": False}),label="结束时间" )
    class Meta:
        model = SalaryCountConfig
        fields  = '__all__'

class SalaryTimeConfig(models.Model): 
  #  iddefaultsChoices = DictConfig.getTypeChoices(type="salary_time_default")
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    #material = models.ForeignKey(Material, db_column='MATERIAL_ID',verbose_name="物料" ,  ) # Field name made lowercase.
    #process = models.ForeignKey(Process, db_column='PROCESS_ID',verbose_name="工艺" ,  ) # Field name made lowercase.
    price = models.DecimalField(db_column='PRICE', max_digits=10, decimal_places=2,verbose_name="单价" ) # Field name made lowercase.
   # isDefault = models.CharField(db_column='IS_DEFAULT', max_length=1, blank=True,verbose_name="是否默认", choices=iddefaultsChoices ) # Field name made lowercase.
  #  startTime = models.DateTimeField( db_column='START_TIME',  blank=True,verbose_name="开始时间"  ) # Field name made lowercase.
   # endTime = models.DateTimeField( db_column='END_TIME',  blank=True,verbose_name="结束时间" ) # Field name made lowercase. 
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True,verbose_name="备注" ) # Field name made lowercase. 
    class Meta:
       # managed = False
        db_table = 'salary_time_config'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2}   remarks {3} ".format(self.id , self.price ,  self.isDefault ,  self.remarks)
 

class SalaryTimeConfigForm(forms.ModelForm): 
 #   startTime =  forms.DateTimeField( required=False,widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm","pickSeconds": False}),label="开始时间" )
  #  endTime =  forms.DateTimeField( required=False,widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm","pickSeconds": False}),label="结束时间" )
    class Meta:
        model = SalaryTimeConfig
        fields  = '__all__' 



class Production(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    terminal = models.ForeignKey('Terminal', db_column='TERMINAL_ID') # Field name made lowercase.
    card = models.ForeignKey(Card, db_column='CARD_ID') # Field name made lowercase.
    employee = models.ForeignKey(Employee, db_column='EMPLOYEE_ID') # Field name made lowercase.
    material = models.ForeignKey(Material, db_column='MATERIAL_ID') # Field name made lowercase.
    process = models.ForeignKey(Process, db_column='PROCESS_ID') # Field name made lowercase.
    time = models.DateTimeField(db_column='TIME') # Field name made lowercase.
    count = models.DecimalField(db_column='COUNT', max_digits=10, decimal_places=2) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'production'

class ReportClass(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    starttime = models.DateTimeField(db_column='STARTTIME') # Field name made lowercase.
    endtime = models.DateTimeField(db_column='ENDTIME') # Field name made lowercase.
    material = models.ForeignKey(Material, db_column='MATERIAL_ID') # Field name made lowercase.
    process_first = models.ForeignKey(Process,   related_name='+' ,  db_column='PROCESS_FIRST_ID', blank=True, null=True) # Field name made lowercase.
    get_count = models.DecimalField(db_column='GET_COUNT', max_digits=10, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    process_last = models.ForeignKey(Process,   related_name='+' ,  db_column='PROCESS_LAST_ID') # Field name made lowercase.
    put_count = models.DecimalField(db_column='PUT_COUNT', max_digits=10, decimal_places=2) # Field name made lowercase.
    average_rate = models.DecimalField(db_column='AVERAGE_RATE', max_digits=10, decimal_places=2) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'report_class'
        
        

class ReportEmployee(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    starttime = models.DateTimeField(db_column='STARTTIME') # Field name made lowercase.
    endtime = models.DateTimeField(db_column='ENDTIME') # Field name made lowercase.
    employee = models.ForeignKey(Employee, db_column='EMPLOYEE_ID') # Field name made lowercase.
    material = models.ForeignKey(Material, db_column='MATERIAL_ID') # Field name made lowercase.
    process_first = models.ForeignKey(Process,  related_name='+'  , db_column='PROCESS_FIRST_ID', blank=True, null=True , ) # Field name made lowercase.
    get_count = models.DecimalField(db_column='GET_COUNT', max_digits=10, decimal_places=2, blank=True, null=True ) # Field name made lowercase.
    process_last = models.ForeignKey(Process, related_name='+', db_column='PROCESS_LAST_ID' ,  ) # Field name made lowercase.
    put_count = models.DecimalField(db_column='PUT_COUNT', max_digits=10, decimal_places=2) # Field name made lowercase.
    average_rate = models.DecimalField(db_column='AVERAGE_RATE', max_digits=10, decimal_places=2) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'report_employee'
