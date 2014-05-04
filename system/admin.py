from django.contrib import admin
from system.models import MaterialType, Material,Employee, SalaryCountConfig, DictConfig

# Register your models here.
admin.site.register(MaterialType)
admin.site.register(Material)
admin.site.register(Employee)
admin.site.register(SalaryCountConfig)
admin.site.register(DictConfig)
