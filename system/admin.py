from django.contrib import admin
from system.models import MaterialType,WorkClass,  Material,Employee, SalaryCountConfig, DictConfig, Card, WorkGroup, Process
from system.models import Production

# Register your models here.
admin.site.register(MaterialType)
admin.site.register(Material)
admin.site.register(Employee)
admin.site.register(SalaryCountConfig)
admin.site.register(DictConfig)
admin.site.register(Card)
admin.site.register(WorkGroup)
admin.site.register(Process)
admin.site.register(Production)
admin.site.register(WorkClass)
