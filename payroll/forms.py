from django import forms

import calculator
from payroll.models import Payroll
from employee.models import Employee


class PayrollForm(forms.Form):
    """
    Form used to create a Payroll object. Uses the calculator to find out what the numbers
    should be.
    
    """
    employee = forms.ModelChoiceField(Employee.objects.all())
    salary = forms.FloatField()
    payperiod = forms.ChoiceField(choices=Employee.PAYPERIOD_CHOICES)
    ei_exempt = forms.BooleanField(required=False)
    cpp_to_date = forms.FloatField()
    ei_to_date = forms.FloatField()
                
    def save(self):
        """
        Save the Payroll data.
        
        """
        # Ask the Payroll calculator what this guy's tax is.
        e = self.cleaned_data["employee"]
        kw = {}
        kw['salary'] = self.cleaned_data['salary']
        kw['ei_exempt'] = self.cleaned_data['ei_exempt'] #not e.subject_to_ei
        kw['cpp_to_date'] = self.cleaned_data['cpp_to_date'] #e.total_cpp_deductions()
        kw['ei_to_date'] = self.cleaned_data['ei_to_date'] #e.total_ei_deductions()
        kw['payperiod'] = self.cleaned_data['payperiod'] #e.payperiod
        
        
        calc = calculator.PayrollCalculator(**kw)
        results = calc.calculate()
        
        # Create the Payroll object.
        payroll_object = Payroll.objects.create(**{
            "employee": e,
            "salary": results[0],
            "ei_insurable_earnings": results[1],
            "taxable_income": results[2],
            "cash_income": results[3],
            "federal_tax_deductions": results[4],
            "provincial_tax_deductions": results[5],
            "additional_tax_deductions": results[6],
            "total_tax_on_income": results[7],
            "cpp_deductions": results[8],
            "ei_deductions": results[9],
            "amounts_deducted_at_source": results[10],
            "total_deductions_on_income": results[11],
            "net_amount": results[12]
        })
        return payroll_object