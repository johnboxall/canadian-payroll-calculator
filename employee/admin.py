from django.contrib import admin
from employee.models import Employee


class EmployeeAdmin(admin.ModelAdmin):    
    list_display = ["__unicode__", 
                    "payroll_link", 
                    "total_salary", 
                    "total_net", 
                    "total_federal_deductions", 
                    "total_provinical_deductions", 
                    "total_cpp_deductions", 
                    "total_ei_deductions", 
                    "total_deductions"]
    
admin.site.register(Employee, EmployeeAdmin)
