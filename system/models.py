# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.deletion import PROTECT
from django.core.urlresolvers import reverse 

from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime
from django.db.models   import Q

from django.core.exceptions import ValidationError


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)




def validate_positive(value):
    if value  <  0:
        raise ValidationError(u'%s 请输入大于0的数字！' % value)
def validate_notnull(value):
    if value  ==  None:
        raise ValidationError(u'%s 必填字段，请输入正确参数！' % value)

       
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

class CardManager(models.Manager): 
    querySql = '''
            SELECT CD.ID ID, CD.NUM NUM ,CD.SHOW_NUM SHOW_NUM,
                 CD.TYPE TYPE ,CD.OWNER_ID OWNER_ID,CD.STATUS STATUS,CD.REMARKS REMARKS,
                IFNULL(IFNULL( IFNULL(PS.NAME,WC.NAME),M.NAME),E.NAME) NAME ,COUNT(C1.SERIAL_NUM) CARD_COUNT
                                    FROM CARDPRT CD 
                                    LEFT JOIN PROCESS PS ON PS.ID = CD.OWNER_ID AND CD.TYPE = '4'
                                    LEFT JOIN WORKCLASS WC ON WC.ID = CD.OWNER_ID AND CD.TYPE IN ('1','2')
                                    LEFT JOIN MATERIAL M  ON M.ID = CD.OWNER_ID AND CD.TYPE = '3'
                                    LEFT JOIN EMPLOYEE E  ON E.ID = CD.OWNER_ID AND CD.TYPE IN ('5','6')
                                    LEFT JOIN CARD C1 ON CD.NUM = C1.NUM
                WHERE 1 = 1
        '''
    def searchCards(self, qdict = [],  **kwargs):
        #if not qdict :
        #    return []
        query = self.querySql
        #logger.info('type' in qdict and qdict.get('type') <> '')
        if  'type' in qdict and qdict.get('type') <> '':
            query += " AND CD.TYPE =  %s " % qdict.get('type')
            #logger.info(qdict.get('type'))
            #logger.info(self.querySql)  
        if  'status' in qdict and qdict.get('status') <> '':
            query += " AND CD.STATUS =  %s " % qdict.get('status') 
        if 'assignd' in  qdict:
            if qdict.get('assignd') == '0':
              query  += " AND ( CD.OWNER_ID IS NULL  OR CD.OWNER_ID = 0 )"
            if qdict.get('assignd') == '1':
               query += " AND  CD.OWNER_ID IS NOT NULL  AND  CD.OWNER_ID <>  0  "
           # logger.info(self.querySql)
        
        if  'num' in qdict and qdict.get('num') <> '' : 
              query += " AND  CD.NUM = '%s'  " % qdict.get('num')
        if  'show_num' in qdict and qdict.get('show_num') <> '' : 
              query += " AND  CD.SHOW_NUM = '%s'  " % qdict.get('show_num')
              
        query += "   group by   ID,  NUM ,  SHOW_NUM,TYPE ,OWNER_ID, STATUS,  REMARKS, NAME "
        query += " order by CD.SHOW_NUM ASC"
        logger.info(query )
        return  list(Card.objects.raw(query))
    def retriveCards(self, **kwargs):
        Card.objects.filter(**kwargs).update(owner_id='0')
    def grantCards(self, owner_id, **kwargs):
        Card.objects.filter(**kwargs).update(owner_id= owner_id)
    def getCard(self, **kwargs):
        return Card.objects.filter(**kwargs)[0]
        

class Card(models.Model):
    objects = CardManager()
    cardTypeChoices = DictConfig.getTypeChoices(type="card_type")
    cardStatusChoices = DictConfig.getTypeChoices(type="card_status")
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20 , verbose_name="卡号"  , editable = False) # Field name made lowercase.
    #serial_num = models.CharField(db_column='SERIAL_NUM' , max_length=20,   editable = False ) # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, choices=cardTypeChoices , editable = False,  verbose_name="卡类型") # Field name made lowercase.
    owner_id = models.IntegerField(db_column='OWNER_ID' ,    blank=True, null=True, verbose_name="所有者"  , editable = False) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1 , choices=cardStatusChoices, verbose_name="状态") # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200 ,   blank=True, verbose_name="备注") # Field name made lowercase.
    color =  models.CharField(db_column='COLOR', max_length=20 , verbose_name="颜色",  editable = False   ) # Field name made lowercase.
    show_num = models.CharField(db_column="SHOW_NUM", max_length=20 , verbose_name="卡表面号",  editable = False )
    class Meta:
        #managed = False
        db_table = 'cardPrt'
    def __unicode__(self):  # Python 3: def __str__(self):
        str = u"{0}({1})({2})".format(self.num, self.color, self.show_num)
        if self.owner_id == 0 or self.owner_id == None:
            str += u'(未分配)'
        else:
            str += u'（已分配）'
        return str 
    @staticmethod
    def getTypeChoices(**kwargs):
        choices = [(card.num,  card.num) for card in Card.objects.filter(**kwargs)] 
        logger.info("cards : %s ", choices)
        return  choices
    @staticmethod
    def getCardChoices1(**kwargs):
      return   [(card.num, card.num   ) for card in
       Card.objects.raw('''
           SELECT ID,NUM,SERIAL_NUM, TYPE,OWNER_ID,STATUS,REMARKS FROM (
                SELECT TMP.* ,
                IF(TMP.NUM = @NUM, @RANK:=@RANK+1,@RANK:=1) RANK,
                 @NUM := TMP.NUM   
                FROM(
                SELECT * FROM CARD C WHERE C.STATUS = 1 ORDER BY C.NUM ASC, C.SERIAL_NUM DESC
                ) TMP  ,(SELECT @RANK,@ROWNUM,@NUM:= NULL ) T
            ) CD
            WHERE CD.RANK = 1  AND  (OWNER_ID = 0  OR OWNER_ID IS NULL)  AND TYPE = %s  
        ''', [kwargs['type']])]
    @staticmethod
    def getCardChoices(**kwargs): 
        return Card.objects.filter(**kwargs).filter(owner_id=0)
        

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
    show_num = forms.CharField(max_length=20, label= u"", widget=forms.TextInput(attrs={'placeholder':'卡表面号'}), required = False )
    type = forms.CharField(max_length=1, widget=forms.Select(choices= [('', '全部')] + typeChoices, attrs={'placeholder':'卡号'}) , label= u"", required = False) # Field name made lowercase.   e 
    assignd = forms.CharField(max_length=1, label = "",  widget=forms.Select( choices= [('', '全部')] + assignedChoices), required = False)
    status = forms.CharField(max_length=1, widget=forms.Select(choices= [('', '全部')] + [('1', '可用'), ('0', '不可用')], attrs={'placeholder':'状态'}) , label= u"", required = False)  
    
    
    
        
class Employee(models.Model):
    
    sexChoices = DictConfig.getTypeChoices(type="sex")
    employeeTypeChoices  = DictConfig.getTypeChoices(type="employee_type")
    statusChoices = DictConfig.getTypeChoices(type="employee_status")  
 
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, verbose_name="员工号",  unique=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, verbose_name="姓名") # Field name made lowercase.
    sex = models.CharField(db_column='SEX', max_length=1, default=1,  verbose_name="性别" , choices=sexChoices  ) # Field name made lowercase.
    idCard = models.CharField(db_column='IDCARD', max_length=20,verbose_name="身份证") # Field name made lowercase.
    tel = models.CharField(db_column='TEL', max_length=20, blank=True,  verbose_name="联系方式") # Field name made lowercase.
    joinTime = models.DateTimeField(db_column='JOIN_TIME'   )#verbose_name="入职时间"
    type = models.CharField(db_column='TYPE', max_length=1, verbose_name="员工类型",  choices=employeeTypeChoices) # Field name made lowercase.   
    status = models.CharField(db_column='STATUS', max_length=1, verbose_name="员工状态" , choices=statusChoices) # Field name made lowercase.
    #card_num1 = models.CharField(db_column='CARD_NUM1', max_length=20,  null=True, blank=True,verbose_name="工作卡号", choices = [('','')]  ) # Field name made lowercase.
    #card_num2 = models.CharField(db_column='CARD_NUM2', max_length=20,  null=True, blank=True,verbose_name="员工卡号", choices = [('','')]  ) # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True,verbose_name="备注") # Field name made lowercase.
    cardprt1 = models.OneToOneField(Card, db_column='CARDPRT1_ID', blank=True, null=True , related_name="employ_card",  verbose_name="工作卡" , limit_choices_to={'type':'5', 'status':'1'})
    cardprt2 = models.OneToOneField(Card, db_column='CARDPRT2_ID', blank=True, null=True, related_name="work_card" ,  verbose_name="员工卡" ,  limit_choices_to={'type':'6', 'status':'1'})
    def full_clean(self, exclude=None, validate_unique=True):
        super(Employee,self).full_clean(exclude=['card_num1', 'card_num2'])
    class Meta:
       # managed = False
        verbose_name = "员工"
        verbose_name_plural = "员工"
        db_table = 'employee'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2}  remarks {3} ".format(self.id , self.num ,  self.name ,  self.remarks )
    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={'pk': self.pk})
    @staticmethod
    def getTypeChoices(**kwargs):
        choices = [(employee.id, u"编号:(%s) 姓名:(%s) 身份证:(%s) " % (employee.num , employee.name, employee.idCard) ) for employee in Employee.objects.filter(**kwargs)] 
        logger.info("cards : %s ", choices)
        return  choices
        

        

class Workshop(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True) # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase.
    @staticmethod
    def getWorkshops(**kwargs):
        choices = [(workshop.id, workshop.name  ) for workshop in Workshop.objects.filter(**kwargs)] 
        return  choices
    class Meta:
     #   managed = False
        db_table = 'workshop'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"名称：({0})  ".format(  self.name )

class WorkGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True) # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase.
    workshop = models.ForeignKey(Workshop, db_column='WORKSHOP_ID', on_delete=PROTECT, blank=True, null=True) # Field name made lowercase.
 
    class Meta:
     #   managed = False
        db_table = 'work_group'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} name {1}  ".format(self.id ,  self.name ) 
  

class MaterialType(models.Model):
    choices = DictConfig.getTypeChoices(type = 'material_type_status')
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20,    unique=True , verbose_name="编号") # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20  , verbose_name="名称") # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, verbose_name="状态", choices=choices) # Field name made lowercase.
    parent = models.ForeignKey('self', db_column='PARENT_ID',   on_delete=PROTECT,  blank=True, null=True, verbose_name="父类型") # Field name made lowercase.
    class Meta:
     #   managed = False
        db_table = 'material_type'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u" 编号：({0}) 名称:({1}) ".format(self.num,self.name )
        
class MaterialTypeForm(forms.ModelForm): 
    statusChoices =  DictConfig.getTypeChoices(type="material_type_status")
    class Meta:
        model = MaterialType
        fields  = [ 'parent','num','name' ,'status',]   
    status = forms.CharField( max_length=1, widget=forms.Select(choices=statusChoices) , label="物料类型状态" ) # Field name made lowercase.                
   # joinTime = forms.DateTimeField(input_formats=input_formats, widget=widgets.SelectDateWidget(),  label="入职时间", )
class NormalSearchForm(forms.Form):
    num = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'编号'}),   label="",  required = False ) # Field name made lowercase.   
    name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'名称'}), label="", required = False ) # Field name made lowercase.  
 


class Material(models.Model):
    statuschoices = DictConfig.getTypeChoices(type = 'material_status') 
    materialType = models.ForeignKey(MaterialType, db_column='MATERIAL_TYPE_ID', on_delete=PROTECT,  verbose_name="类型") # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20 , unique=True, verbose_name="编号") # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, verbose_name="名称") # Field name made lowercase.
    
    #def clean_fields(self, exclude=None):
    #    return super(Material,self).clean_fields( exclude=['card_num'])
    
  
   # conver = models.IntegerField(db_column='CONVER', blank=True, null=True,  verbose_name="换算") # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True , choices=statuschoices) # Field name made lowercase.
    #card_num = models.CharField(db_column='CARD_NUM', max_length=20,  blank=True, choices = [('','')] ,    null=True, verbose_name="物料卡编号") # Field name made lowercase.
    cardprt = models.OneToOneField(Card, db_column='CARDPRT_ID', on_delete=PROTECT, blank=True, null=True, verbose_name="物料卡"  , limit_choices_to={'type':'3', 'status':'1'}) # Field name made lowercase.
    
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True, verbose_name="备注") # Field name made lowercase.
    class Meta:
       # managed = False
        verbose_name = "物料"
        verbose_name_plural = "物料"
        db_table = 'material'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u" 编号({0}) 名称({1}) ".format(  self.num ,  self.name    )
    @staticmethod
    def getMaterialChoices( **kwargs):
        return [(material.id, material) for material in Material.objects.filter(**kwargs)]

   
class MaterialForm(forms.ModelForm): 
    statusChoices =  DictConfig.getTypeChoices(type="material_status")
   # modeChoices =  DictConfig.getTypeChoices(type="material_mode") 
    class Meta:
        model = Material
        fields  = '__all__'
    status = forms.CharField( max_length=1, widget=forms.Select(choices=statusChoices) , label="物料状态" ) # Field name made lowercase. 
    #mode = forms.CharField( max_length=1, widget=forms.Select(choices=modeChoices) , label="统计方式" ) # Field name made lowercase.  
    #card_num =  forms.ChoiceField(choices= Card.getCardChoices(type='3'),  label="工作卡号", required=False )    
   

 
class Process(models.Model):
    processIsFirstchoices = DictConfig.getTypeChoices(type = 'process_isfirst')
    statuschoices = DictConfig.getTypeChoices(type = 'process_status')
    modechoices = DictConfig.getTypeChoices(type = 'process_mode')
    #unitchoices = DictConfig.getTypeChoices(type = 'material_mode')    
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, unique=True, verbose_name="编号") # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, verbose_name="名称") # Field name made lowercase.
    firstProcess = models.ForeignKey('self', db_column='FIRST_PROCESS_ID', on_delete=PROTECT, limit_choices_to={'isFirst' : '1'} ,  blank=True, null=True, verbose_name="前工艺") # Field name made lowercase.
    isFirst = models.CharField(db_column='IS_FIRST', max_length=1, choices=processIsFirstchoices, verbose_name="是否前工艺"  ) # Field name made lowercase.    
    status = models.CharField(db_column='STATUS', max_length=1, default=1, choices=statuschoices, verbose_name="状态") # Field name made lowercase.
    #card_num = models.CharField(db_column='CARD_NUM', max_length=20, blank=True, null=False, verbose_name="工艺卡号",  choices = [('','')]   ) # Field name made lowercase.
    cardprt = models.OneToOneField(Card, db_column='CARDPRT_ID', on_delete=PROTECT, blank=True, null=True, verbose_name="工艺卡"    , limit_choices_to={'type':'4', 'status':'1'}) # Field name made lowercase.
    mode = models.CharField(db_column='MODE', max_length=1,  verbose_name="统计方式", choices=modechoices) # Field name made lowercase
    unit = models.CharField(db_column='UNIT', max_length=20,  verbose_name="单位"  ) # Field name made lowercase..
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True, verbose_name="备注") # Field name made lowercase.
    def clean_fields(self, exclude=None):
        return super(Process,self).clean_fields(exclude=['card_num'])
    class Meta:
       # managed = False
        verbose_name = "工艺"
        verbose_name_plural = "工艺"
        db_table = 'process'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u" 编号({0})  名称({1}) ".format( self.num ,  self.name  )
    @staticmethod
    def getProcessChoices( **kwargs):
        return [(process.id, process ) for process in Process.objects.filter(**kwargs)]
    @staticmethod
    def getUnitChoices():
       return  [(unit.unit, unit.unit  ) for unit in
        Process.objects.raw('''SELECT ID,UNIT FROM  (
                                    SELECT TMP.* ,
                                        IF(TMP.UNIT = @UNIT, @RANK:=@RANK+1,@RANK:=1) RANK,
                                         @UNIT := TMP.UNIT    FROM 
                                    (SELECT ID, UNIT FROM PROCESS P ORDER BY UNIT ) TMP, (SELECT @RANK,@ROWNUM,@UNIT:=NULL) T 
                                    ) CD
                                    WHERE CD.RANK =1 
                            ''')]

class ProcessForm(forms.ModelForm):  
    class Meta:
        model = Process
        fields  =  ['num', 'name', 'firstProcess', 'isFirst', 'status', 'cardprt', 'mode', 'unit', 'remarks']
    '''
    def __init__(self, *args, **kwargs):
        super(ProcessForm, self).__init__(*args, **kwargs)
        self.fields['card_num'] = forms.ChoiceField(   choices=[('', '---------')] + Card.getCardChoices(type="4") ,  label="工艺卡号", required=False )
    '''
    def clean(self):
        cleand_data = super(ProcessForm, self).clean()
        isFirst = cleand_data.get('isFirst')
        firstProcess = cleand_data.get("firstProcess")
        #card_num = cleand_data.get("card_num")
        #logger.info(cleand_data)
        #logger.info(card_num)
        mode = cleand_data.get("mode")
        if isFirst == '1' and firstProcess:
            self._errors["firstProcess"] = self.error_class([u"只有后工艺类型可以选择前工艺！"])
            del cleand_data['firstProcess']
        if isFirst == '0' and firstProcess and mode <> firstProcess.mode:
            logger.info(u"firstProcess:%s mode:%s firstProcess.mode:%s", firstProcess, mode, firstProcess.mode)
            self._errors["mode"] = self.error_class([u"后工艺统计方式必须与前工艺保持一致！"])
            del cleand_data['mode']
        return cleand_data

         
class Terminal(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, blank=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True) # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, blank=True) # Field name made lowercase.
    workGroup = models.ForeignKey(WorkGroup, db_column='WORKGROUP_ID', on_delete=PROTECT, blank=True, null=True) # Field name made lowercase.
    ip1 = models.CharField(db_column='IP1', max_length=20, blank=True) # Field name made lowercase.
    ip2 = models.CharField(db_column='IP2', max_length=20, blank=True) # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase.
    defaultMaterial = models.ForeignKey(Material, db_column='DEFAULT_MATERIAL_ID', on_delete=PROTECT, blank=True, null=True) # Field name made lowercase.
    defaultProcess = models.ForeignKey(Process, db_column='DEFAULT_PROCESS_ID', on_delete=PROTECT, blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'terminal'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2}   remarks {3} ".format(self.id , self.num ,  self.name ,  self.remarks)
        


class EmployeeForm(forms.ModelForm):
    #sexChoices = DictConfig.getTypeChoices(type="sex") 
    employeeTypeChoices  = DictConfig.getTypeChoices(type="employee_type")
    statusChoices = DictConfig.getTypeChoices(type="employee_status")
    joinTime = forms.DateTimeField(  widget=DateTimePicker(options={"format": "YYYY-MM-DD","pickSeconds": False}),label="入职时间" )
    def clean(self): 
        cleand_data = super(EmployeeForm, self).clean() 
        cardprt1 = cleand_data.get('cardprt1')
        type = cleand_data.get('type')
        if cardprt1 and type <> '1':
            self._errors["cardprt1"] = self.error_class([u"%s卡片只能分配给计件工，请重新选择！" %  cardprt1.show_num ])
        return cleand_data; 
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
       # self.fields['sex'] = forms.ChoiceField(choices=DictConfig.getTypeChoices(type='sex'), label="性别", )
        #self.fields['card_num1'] = forms.ChoiceField(choices= [('', '------')] + Card.getCardChoices(type='5'),  label="工作卡号", required=False )
       # self.fields['card_num2'] = forms.ChoiceField(choices= [('', '------')] + Card.getCardChoices(type='6'),   label="员工卡号", required=False )
    class Meta:
        model = Employee
        fields  = ['num', 'name', 'idCard','sex', 'tel','joinTime' , 'type', 'status', 'cardprt1', 'cardprt2', 'remarks',   ]
       
    #sex = forms.CharField(max_length=1 ,  label="性别") # Field name made lowercase.    
    type = forms.CharField(max_length=1, widget=forms.Select(choices=employeeTypeChoices) , label="员工类型", ) # Field name made lowercase.   
    status = forms.CharField( max_length=1, widget=forms.Select(choices=statusChoices) , label="员工状态" ) # Field name made lowercase.    
    
        
    input_formats = ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
        '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
        '%Y-%m-%d',              # '2006-10-25'
        ]
   
class EmployeeSearchForm(forms.Form):
    num = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'工号'}),   label="",  required = False ) # Field name made lowercase.   
    name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'姓名'}), label="", required = False ) # Field name made lowercase.  
    card_num1 = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'工作卡号'}), label="", required = False ) # Field name made lowercase.  
    def __init__(self, *args, **kwargs):
        super(EmployeeSearchForm,self).__init__(*args, **kwargs)
        statusChoices = DictConfig.getTypeChoices(type="employee_status") 
        self.fields['status'] = forms.CharField(widget=forms.Select(attrs={'placeholder':'状态'}, choices=[('', '全部')] + statusChoices),   label="",  required = False ) # Field name made lowercase.   
    
    


class WorkClass(models.Model):    
    clasTypeChoices = DictConfig.getTypeChoices(type="class_type")
    classStatusTypeChoices  = DictConfig.getTypeChoices(type="class_status")    
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, unique=True, verbose_name="编号",) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True, verbose_name="名称",) # Field name made lowercase.
    workshop = models.ForeignKey(Workshop, db_column='WORKSHOP_ID' , on_delete=PROTECT,  verbose_name="车间",) # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, blank=True, verbose_name="类型",  choices=clasTypeChoices) # Field name made lowercase.   
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, verbose_name="状态", choices=classStatusTypeChoices) # Field name made lowercase.
    #card_num = models.CharField(db_column='CARD_NUM', max_length=20,  null=True, verbose_name="班次卡号", blank=True, choices=[('','')]) # Field name made lowercase. 
    cardprt = models.OneToOneField(Card, db_column='CARDPRT_ID', on_delete=PROTECT, blank=True, null=True, verbose_name="班次卡"   , limit_choices_to= ( Q(type__in=['1', '2'])& Q(status='1') )  ) # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, verbose_name="备注", blank=True) # Field name made lowercase.     
    def clean_fields(self, exclude=None):
        return super(WorkClass,self).clean_fields( exclude=['card_num'])
    class Meta:
       # managed = False
        verbose_name = "班次"
        verbose_name_plural = "班次"
        db_table = 'workclass'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"编号：{0} 类型：{1} 名称：{2} ".format( self.num , self.get_type_display(), self.name)
    @staticmethod
    def getTypeChoices(**kwargs): 
        choices = [(clz.id, u"编号:(%s) 名称:(%s) " % (clz.num , clz.name) ) for clz in WorkClass.objects.filter(**kwargs)] 
        logger.info("cards : %s ", choices)
        return  choices    


class WorkClassForm(forms.ModelForm):  
    class Meta:
        model = WorkClass
        fields  = '__all__'
    '''
    def __init__(self, *args, **kwargs):
        super(WorkClassForm, self).__init__(*args, **kwargs)
        self.fields['card_num']  = forms.ChoiceField( choices= [('', '------')] + Card.getCardChoices(type=1) + Card.getCardChoices(type=2),  label="班次卡", required=False )
    '''   
        
 

class Workshift(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    terminal = models.ForeignKey(Terminal, db_column='TERMINAL_ID' , on_delete=PROTECT,) # Field name made lowercase.
    card = models.ForeignKey(Card, db_column='CARD_ID' , on_delete=PROTECT,) # Field name made lowercase.
    time = models.DateTimeField(db_column='TIME') # Field name made lowercase.
    workclass = models.ForeignKey(WorkClass, db_column='WORKCLASS_ID' , on_delete=PROTECT,) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'workshift'

class Attendance(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    terminal = models.ForeignKey('Terminal', db_column='TERMINAL_ID', on_delete=PROTECT,) # Field name made lowercase.
    employee = models.ForeignKey('Employee', db_column='EMPLOYEE_ID', on_delete=PROTECT,) # Field name made lowercase.
    card = models.ForeignKey('Card', db_column='CARD_ID', on_delete=PROTECT,) # Field name made lowercase.
    time = models.DateTimeField(db_column='TIME') # Field name made lowercase.
    class Meta:
        #managed = False
        db_table = 'attendance'

  

class SalaryCountConfig(models.Model): 
    iddefaultsChoices = DictConfig.getTypeChoices(type="salary_count_default")
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    material = models.ForeignKey(Material, db_column='MATERIAL_ID',verbose_name="物料" , on_delete=PROTECT,  ) # Field name made lowercase.
    process = models.ForeignKey(Process, db_column='PROCESS_ID',verbose_name="工艺", on_delete=PROTECT,  ) # Field name made lowercase.
    price = models.DecimalField(db_column='PRICE', max_digits=10, decimal_places=2,verbose_name="单价", validators=[validate_positive] ) # Field name made lowercase.
   # isDefault = models.CharField(db_column='IS_DEFAULT', max_length=1, blank=True,verbose_name="是否默认", choices=iddefaultsChoices ) # Field name made lowercase.
   # startTime = models.DateTimeField(db_column='START_TIME',  blank=True,verbose_name="开始时间"  ) # Field name made lowercase.
   # endTime = models.DateTimeField( db_column='END_TIME',  blank=True,verbose_name="结束时间" ) # Field name made lowercase. 
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True,verbose_name="备注" ) # Field name made lowercase. 
    #unit = models.CharField(db_column='UNIT', max_length=20, blank=True)
    class Meta:
       # managed = False
        db_table = 'salary_count_config'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} remarks {2}   ".format(self.id , self.price ,  self.remarks)
 

class SalaryCountConfigForm(forms.ModelForm): 
   # startTime = forms.DateTimeField( required=False,widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm","pickSeconds": False}),label="开始时间" )
  #  endTime =  forms.DateTimeField( required=False,widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm","pickSeconds": False}),label="结束时间" )
    class Meta:
        model = SalaryCountConfig
        fields  = '__all__'
    def __init__(self, *args,  **kwargs):
        super(SalaryCountConfigForm, self).__init__(*args, **kwargs)
        #self.fields['unit'] = forms.ChoiceField( required = False, label ='单位' , choices= Process.getUnitChoices())
        
class SalaryCountSearchForm(forms.Form): 
    #num = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'工号'}),   label="",  required = False ) # Field name made lowercase.   
    #name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'姓名'}), label="", required = False ) # Field name made lowercase.  
       
   
    def __init__(self, *args, **kwargs):
        super(SalaryCountSearchForm, self).__init__(*args, **kwargs)
        self.fields['material'] = forms.ChoiceField(required = False, choices= [('', ' 全部物料')] + Material.getMaterialChoices(),  label="")
        self.fields['process'] = forms.ChoiceField(required = False, choices= [('', ' 全部工艺')] + Process.getProcessChoices(),  label="")


class SalaryTimeConfig(models.Model): 
  #  iddefaultsChoices = DictConfig.getTypeChoices(type="salary_time_default")
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    #material = models.ForeignKey(Material, db_column='MATERIAL_ID',verbose_name="物料" ,  ) # Field name made lowercase.
    #process = models.ForeignKey(Process, db_column='PROCESS_ID',verbose_name="工艺" ,  ) # Field name made lowercase.
    price = models.DecimalField(db_column='PRICE', max_digits=10, decimal_places=2,verbose_name="单价" , validators=[validate_positive]) # Field name made lowercase.
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
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    terminal = models.ForeignKey('Terminal', db_column='TERMINAL_ID' , on_delete=PROTECT) # Field name made lowercase.
    card = models.ForeignKey(Card, db_column='CARD_ID' , on_delete=PROTECT) # Field name made lowercase.
    employee = models.ForeignKey(Employee, db_column='EMPLOYEE_ID' , on_delete=PROTECT,) # Field name made lowercase.
    material = models.ForeignKey(Material, db_column='MATERIAL_ID' , on_delete=PROTECT) # Field name made lowercase.
    process = models.ForeignKey(Process, db_column='PROCESS_ID' , on_delete=PROTECT) # Field name made lowercase.
    time = models.DateTimeField(db_column='TIME') # Field name made lowercase.
    count = models.DecimalField(db_column='COUNT', max_digits=10, decimal_places=2) # Field name made lowercase.
    class Meta:
        #managed = False
        db_table = 'production'

class ProductionSearchForm(forms.Form): 
    #employee_num = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'工号'}),   label="",  required = False ) # Field name made lowercase.   
    #employee_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'姓名'}), label="", required = False ) # Field name made lowercase.  
    #material = forms.ChoiceField(required = False, choices= [('', ' 全部物料')]  ,  label="")
    #process = forms.ChoiceField(required = False, choices= [('', ' 全部工艺')]  ,  label="")
    
    def __init__(self, *args, **kwargs): 
        super(ProductionSearchForm, self).__init__(*args, **kwargs)
        self.fields['workshop'] = forms.ChoiceField(required = False, choices= [('', ' 全部车间')] + Workshop.getWorkshops(),  label="")
        self.fields['material'] = forms.ChoiceField(required = False, choices= [('', ' 全部物料')] + Material.getMaterialChoices(),  label="")
        self.fields['process'] = forms.ChoiceField(required = False, choices= [('', ' 全部工艺')] + Process.getProcessChoices(),  label="") 
        self.fields['is_first'] = forms.ChoiceField( required = False, label="", choices=[('', '全部'), ('0', '交料'),('1', '领料')] ,  )
        self.fields['employee_num'] = forms.CharField(max_length=20,widget=forms.TextInput(attrs={ 'size':'10','placeholder':'工号'}),   label="",  required = False ) # Field name made lowercase.         
        self.fields['employee_name'] = forms.CharField(max_length=20,widget=forms.TextInput(attrs={  'size':'13','placeholder':'姓名'}), label="", required = False ) # Field name made lowercase. 
        self.fields['start_time'] = forms.DateTimeField( required = False,  widget=DateTimePicker( div_attrs={'class':'input-group date  ' ,  },  attrs={ 'value':datetime.now().strftime('%Y-%m-%d'),  "class": "form-control ",'placeholder':'开始时间'   },  options={"format": "YYYY-MM-DD","pickSeconds": False}),label="" )
        self.fields['end_time'] = forms.DateTimeField( required = False  ,  widget=DateTimePicker( div_attrs={'class':'input-group date  ' ,  }, attrs={ 'value':datetime.now().strftime('%Y-%m-%d'),'placeholder':'结束时间',  "class": "form-control "  }, options={"format": "YYYY-MM-DD","pickSeconds": False}),label="" )
        
        




class ReportClass(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    starttime = models.DateTimeField(db_column='STARTTIME') # Field name made lowercase.
    endtime = models.DateTimeField(db_column='ENDTIME') # Field name made lowercase.
    material = models.ForeignKey(Material, db_column='MATERIAL_ID' , on_delete=PROTECT) # Field name made lowercase.
    process_first = models.ForeignKey(Process,   related_name='+' ,  on_delete=PROTECT, db_column='PROCESS_FIRST_ID', blank=True, null=True) # Field name made lowercase.
    get_count = models.DecimalField(db_column='GET_COUNT', max_digits=10, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    process_last = models.ForeignKey(Process,   related_name='+' , on_delete=PROTECT,  db_column='PROCESS_LAST_ID') # Field name made lowercase.
    put_count = models.DecimalField(db_column='PUT_COUNT', max_digits=10, decimal_places=2) # Field name made lowercase.
    average_rate = models.DecimalField(db_column='AVERAGE_RATE', max_digits=10, decimal_places=2) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'report_class'
        
        

class ReportEmployee(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    starttime = models.DateTimeField(db_column='STARTTIME') # Field name made lowercase.
    endtime = models.DateTimeField(db_column='ENDTIME') # Field name made lowercase.
    employee = models.ForeignKey(Employee, on_delete=PROTECT, db_column='EMPLOYEE_ID') # Field name made lowercase.
    material = models.ForeignKey(Material, on_delete=PROTECT, db_column='MATERIAL_ID') # Field name made lowercase.
    process_first = models.ForeignKey(Process, on_delete=PROTECT,  related_name='+'  , db_column='PROCESS_FIRST_ID', blank=True, null=True , ) # Field name made lowercase.
    get_count = models.DecimalField(db_column='GET_COUNT', max_digits=10, decimal_places=2, blank=True, null=True ) # Field name made lowercase.
    process_last = models.ForeignKey(Process, on_delete=PROTECT, related_name='+', db_column='PROCESS_LAST_ID' ,  ) # Field name made lowercase.
    put_count = models.DecimalField(db_column='PUT_COUNT', max_digits=10, decimal_places=2) # Field name made lowercase.
    average_rate = models.DecimalField(db_column='AVERAGE_RATE', max_digits=10, decimal_places=2) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'report_employee'
        
class ReportEmployeeSearchForm(forms.Form):      
    def __init__(self, *args, **kwargs): 
        super(ReportEmployeeSearchForm, self).__init__(*args, **kwargs)
        self.fields['workshop'] = forms.ChoiceField(required = False, choices= [('', ' 全部车间')] + Workshop.getWorkshops(),  label="")
        self.fields['material'] = forms.ChoiceField(required = False, choices= [('', ' 全部物料')] + Material.getMaterialChoices(),  label="")
        self.fields['process'] = forms.ChoiceField(required = False, choices= [('', ' 全部工艺')] + Process.getProcessChoices(),  label="") 
        #self.fields['is_first'] = forms.ChoiceField( required = False, label="", choices=[('', '全部'), ('0', '交料'),('1', '领料')] ,  )
        self.fields['employee_num'] = forms.CharField(max_length=20,widget=forms.TextInput(attrs={ 'size':'17','placeholder':'工号'}),   label="",  required = False ) # Field name made lowercase.         
        self.fields['employee_name'] = forms.CharField(max_length=20,widget=forms.TextInput(attrs={  'size':'20','placeholder':'姓名'}), label="", required = False ) # Field name made lowercase. 
        self.fields['start_time'] = forms.DateTimeField( required = False,   validators=[validate_notnull],   widget=DateTimePicker( div_attrs={'class':'input-group date '},  attrs={ 'value':datetime.now().replace(month=datetime.now().month - 1).strftime('%Y-%m-%d'),  "class": "form-control",'placeholder':'开始时间'}, options={"format": "YYYY-MM-DD","pickSeconds": False}),label="" )
        self.fields['end_time'] = forms.DateTimeField( required = False ,  validators=[validate_notnull],   widget=DateTimePicker( div_attrs={'class':'input-group date '}, attrs={ 'value':datetime.now().strftime('%Y-%m-%d'),'placeholder':'结束时间',  "class": "form-control",}, options={"format": "YYYY-MM-DD","pickSeconds": False}),label="" )
        


       
class ReportClassSearchForm(forms.Form):      
    def __init__(self, *args, **kwargs): 
        super(ReportClassSearchForm, self).__init__(*args, **kwargs)
        self.fields['workshop'] = forms.ChoiceField(required = False, choices= [('', ' 全部车间')] + Workshop.getWorkshops(),  label="")
        self.fields['material'] = forms.ChoiceField(required = False, choices= [('', ' 全部物料')] + Material.getMaterialChoices(),  label="")
        self.fields['process'] = forms.ChoiceField(required = False, choices= [('', ' 全部工艺')] + Process.getProcessChoices(),  label="") 
        #self.fields['is_first'] = forms.ChoiceField( required = False, label="", choices=[('', '全部'), ('0', '交料'),('1', '领料')] ,  )
        self.fields['start_time'] = forms.DateTimeField( required = False, validators=[validate_notnull],      widget=DateTimePicker( div_attrs={'class':'input-group date '},  attrs={ 'value':datetime.now().replace(month=datetime.now().month - 1).strftime('%Y-%m-%d'),  "class": "form-control",'placeholder':'开始时间'}, options={"format": "YYYY-MM-DD","pickSeconds": False}),label="" )
        self.fields['end_time'] = forms.DateTimeField( required = False  , validators=[validate_notnull],  widget=DateTimePicker( div_attrs={'class':'input-group date '}, attrs={ 'value':datetime.now().strftime('%Y-%m-%d'),'placeholder':'结束时间',  "class": "form-control",}, options={"format": "YYYY-MM-DD","pickSeconds": False}),label="" )
     


@receiver(pre_save, sender=MaterialType)
def make_material_type_num(sender, instance, raw, **kwargs):
    logger.info("%s", instance.parent)
    if instance.id is None:        
        if instance.parent:
            #instance.num =   instance.parent.num  +  '.' +   instance.num
            pass 

@receiver(pre_save, sender=Material)
def make_material_num(sender, instance, raw, **kwargs):
    logger.info("%s", instance.materialType)
    if instance.id is None:        
        if instance.materialType:
            #instance.num =   instance.materialType.num  +  '.' +   instance.num 
            pass
