from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect


class EmployeeFormPreview(FormPreview):
    def done(self, request, clean_data):
        return HttpResponseRedirect('/form/success')
        
        
