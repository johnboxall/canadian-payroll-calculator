from string import split as L
from django.contrib import admin
from django.contrib.admin import helpers
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response

from payroll.models import Payroll
from payroll.forms import PayrollForm
from employee.models import Employee


class PayrollAdmin(admin.ModelAdmin):
    list_display = L("employee salary net_amount federal_tax_deductions provincial_tax_deductions cpp_deductions ei_deductions total_tax_on_income total_deductions_on_income corporate_payable_tax paid created_at")
    
    list_filter = L("employee paid")
    actions = L("mark_as_paid")
    ordering = L("-created_at")
    date_hierarchy = "created_at"
    save_as = True


    def mark_as_paid(self, request, qs):
        updates = qs.update(paid=True)
        self.message_user(request, "%s successfully marked as paid." % updates)
    mark_as_paid.short_description = "Mark selected payrolls as paid"

    def add_view(self, request, form_url='', extra_context=None):
        """Copied from django.auth.admin.UserAdmin.add_view."""
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise PermissionDenied        
        
        if request.method == "POST":
            form = PayrollForm(request.POST)
            if form.is_valid():
                payroll = form.save()
                self.log_addition(request, payroll)
                return self.response_add(request, payroll)
                
        else:
            initial = None
            if 'employee_id' in request.REQUEST:            
                e = Employee.objects.get(pk=request.REQUEST['employee_id'])
                initial = {"employee": e.id,
                           "salary": e.salary,
                           "ei_exempt": not e.subject_to_ei,
                           "cpp_to_date": e.total_cpp_deductions(),
                           "ei_to_date": e.total_ei_deductions(),
                           "payperiod": e.payperiod}
            form = PayrollForm(initial=initial)

        return render_to_response('admin/payroll/payroll/add_form.html', {
            'title': 'Add Payroll Entry',
            'form': form,
            'is_popup': request.REQUEST.has_key('_popup'),
            'add': True,
            'change': False,
            'has_add_permission': True,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_file_field': False,
            'has_absolute_uri': False,
            'auto_populated_fields': (),
            'opts': self.model._meta,
            'save_as': False,
            'root_path': self.admin_site.root_path,
            'app_label': self.model._meta.app_label,
        }, context_instance=RequestContext(request))
    

admin.site.register(Payroll, PayrollAdmin)
