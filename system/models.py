from django.db import models



       
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
            


sexChoices = DictConfig.objects.filter(type="sex")
employeeTypeChoices  = DictConfig.objects.filter(type="employee_type")
statusChoices = DictConfig.objects.filter(type="employee_status")


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
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, blank=True) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True) # Field name made lowercase.
    parent = models.ForeignKey('self', db_column='PARENT_ID', blank=True, null=True) # Field name made lowercase.
    class Meta:
     #   managed = False
        db_table = 'material_type'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} status {2} ".format(self.id ,  self.num ,  self.status)
        
class Material(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, blank=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True) # Field name made lowercase.
    materialType = models.ForeignKey(MaterialType, db_column='MATERIAL_TYPE_ID', blank=True, null=True) # Field name made lowercase.
    mode = models.CharField(db_column='MODE', max_length=1, blank=True) # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=20, blank=True) # Field name made lowercase.
    conver = models.IntegerField(db_column='CONVER', blank=True, null=True) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True) # Field name made lowercase.
    card_num = models.CharField(db_column='CARD_NUM', max_length=20, blank=True) # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase.
    class Meta:
       # managed = False
        db_table = 'material'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2} conver {3} mode {4} card_num {5} remarks {6} ".format(self.id , self.num ,  self.name ,  self.conver ,  self.mode ,  self.card_num ,  self.remarks)
 
 
class Process(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, blank=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True) # Field name made lowercase.
    firstProcess = models.ForeignKey('self', db_column='FIRST_PROCESS_ID', blank=True, null=True) # Field name made lowercase.
    isFirst = models.CharField(db_column='IS_FIRST', max_length=1, blank=True) # Field name made lowercase.    
    status = models.CharField(db_column='STATUS', max_length=1, blank=True) # Field name made lowercase.
    card_num = models.CharField(db_column='CARD_NUM', max_length=20, blank=True) # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase.
    class Meta:
       # managed = False
        db_table = 'process'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2}  card_num {3} remarks {4} ".format(self.id , self.num ,  self.name ,   self.card_num ,  self.remarks)
 
         
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
       # managed = False
        db_table = 'terminal'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2}   remarks {3} ".format(self.id , self.num ,  self.name ,  self.remarks)
        
        

         
class Employee(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, blank=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True) # Field name made lowercase.
    sex = models.CharField(db_column='SEX', max_length=1, blank=True) # Field name made lowercase.
    idCard = models.CharField(db_column='IDCARD', max_length=20, blank=True) # Field name made lowercase.
    tel = models.CharField(db_column='TEL', max_length=20, blank=True) # Field name made lowercase.
    joinTime = models.DateTimeField(auto_now=True, db_column='JOIN_TIME' , blank=True)
    type = models.CharField(db_column='TYPE', max_length=1, blank=True) # Field name made lowercase.   
    status = models.CharField(db_column='STATUS', max_length=1, blank=True) # Field name made lowercase.
    cardNum1 = models.CharField(db_column='CARD_NUM1', max_length=20, blank=True) # Field name made lowercase.
    cardNum2 = models.CharField(db_column='CARD_NUM2', max_length=20, blank=True) # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase.
     
    class Meta:
       # managed = False
        db_table = 'employee'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2}  remarks {3} ".format(self.id , self.num ,  self.name ,  self.remarks)
        
        
class WorkClass(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, blank=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True) # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, blank=True) # Field name made lowercase.   
    status = models.CharField(db_column='STATUS', max_length=1, blank=True) # Field name made lowercase.
    cardNum = models.CharField(db_column='CARD_NUM', max_length=20, blank=True) # Field name made lowercase. 
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase.     
    class Meta:
       # managed = False
        db_table = 'work_class'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2}   remarks {3} ".format(self.id , self.num ,  self.name ,  self.remarks)
        

class CardType(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True) # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, blank=True) # Field name made lowercase.   
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase.     
    class Meta:
     #   managed = False
        db_table = 'card_type'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} name {1} status {2} ".format(self.id ,  self.name ,  self.status)
        
 
class Card(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    num = models.CharField(db_column='NUM', max_length=20, blank=True) # Field name made lowercase.
    serialNum = models.IntegerField(db_column='SERIAL_NUM',  blank=True,  null=True, unique=True) # Field name made lowercase.
    cardType = models.ForeignKey(CardType, db_column='CARD_TYPE_ID', blank=True, null=True) # Field name made lowercase.
    ownerId = models.IntegerField(db_column='OWNER_ID',  blank=True,  null=True) # Field name made lowercase. 
    status = models.CharField(db_column='STATUS', max_length=1, blank=True) # Field name made lowercase. 
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase.
    class Meta:
       # managed = False
        db_table = 'card'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2} remarks {3} ".format(self.id , self.num ,  self.remarks)
        
        

class SalaryCountConfig(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) # Field name made lowercase.
    material = models.ForeignKey(Material, db_column='MATERIAL_ID', blank=True, null=True) # Field name made lowercase.
    process = models.ForeignKey(Process, db_column='PROCESS_ID', blank=True, null=True) # Field name made lowercase.
    price = models.DecimalField(db_column='PRICE', max_digits=10, decimal_places=2) # Field name made lowercase.
    isDefault = models.CharField(db_column='IS_DEFAULT', max_length=1, blank=True) # Field name made lowercase.
    startTime = models.DateTimeField(auto_now=True, db_column='START_TIME',  blank=True) # Field name made lowercase.
    endTime = models.DateTimeField(auto_now=True, db_column='END_TIME',  blank=True) # Field name made lowercase. 
    remarks = models.TextField(db_column='REMARKS', max_length=200, blank=True) # Field name made lowercase. 
    class Meta:
       # managed = False
        db_table = 'salary_count_config'
    def __unicode__(self):  # Python 3: def __str__(self):
        return  u"id {0} num {1} name {2}   remarks {3} ".format(self.id , self.price ,  self.isDefault ,  self.remarks)
        
 
    

from django import forms
class EmployeeForm(forms.Form):
    class Meta:
        model = Employee
    sex = forms.CharField(max_length=1, widget=forms.Select(choices=sexChoices)) # Field name made lowercase.    
    type = forms.CharField(max_length=1, widget=forms.Select(choices=employeeTypeChoices)) # Field name made lowercase.   
    status = forms.CharField( max_length=1, widget=forms.Select(choices=statusChoices) ) # Field name made lowercase.
    
    
    
