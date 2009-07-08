from django.db import models
from django.db.models import Sum


class Employee(models.Model):
    """
    A dude who works with you!
    
    """
    # This logic would be better in the calculator.
    PAYPERIOD_CHOICES = (
        (0, "Daily (240)"),
        (1, "Weekly (52)"),
        (2, "Biweekly (26)"),
        (3, "Semi-monthly (24)"),
        (4, "Monthly (12)"),
        (5, "10 pay periods a year"),
        (6, "13 pay periods a year"),
        (7, "22 pay periods a year"),
        (8, "Weekly (53)"),
        (9, "Biweekly (27)"),)
    PAYPERIOD_DEFAULT = PAYPERIOD_CHOICES[4][0]

    FEDERAL_CLAIMCODE_CHOICES = (
        (1, "Claim Code 1 (Minimum - 10,100.00)"),
        (2, "Claim Code 2 (10,100.01 - 12,072.00)"),
        (3, "Claim Code 3 (12,072.01 - 14,044.00)"),
        (4, "Claim Code 4 (14,044.01 - 16,016.00)"),
        (5, "Claim Code 5 (16,016.01 - 17,988.00)"),
        (6, "Claim Code 6 (17,988.01 - 19,960.00)"),
        (7, "Claim Code 7 (19,960.01 - 21,932.00)"),
        (8, "Claim Code 8 (21,932.01 - 23,904.00)"),
        (9, "Claim Code 9 (23,904.01 - 25,876.00)"),
        (10, "Claim Code 10 (25,876.01 - 27,848.00)"),
        (11, "Claim Code E (No tax)"),)
    FEDERAL_CLAIMCODE_DEFAULT = FEDERAL_CLAIMCODE_CHOICES[0][0]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    salary = models.FloatField(default="0.00", help_text="Default salary per pay period.")
    payperiod = models.SmallIntegerField(choices=PAYPERIOD_CHOICES, default=PAYPERIOD_DEFAULT, help_text="Default pay period.")
    federal_claim_code = models.SmallIntegerField(choices=FEDERAL_CLAIMCODE_CHOICES, default=FEDERAL_CLAIMCODE_DEFAULT, help_text="Default claim code.")    
    # ### Provincal claim codes change depending on what province this dude is from.
    # provinical_claim_code = ""
    subject_to_ei = models.BooleanField(default=True, help_text="Where this employee is subject to EI.") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)
        
    def get_add_payroll_url(self):
        return "/payroll/payroll/add/?employee_id=%i" % self.id
    
    def payroll_link(self):
        return '<a href="%s">Add</a>' % self.get_add_payroll_url()
    payroll_link.allow_tags = True 

    def _payroll_field_sum(self, field):
        """
        Return the total of a field
        
        """
        total = self.payroll_set.aggregate(total=Sum(field)).get("total") or 0.0
        return round(total, 3)
    
    def total_salary(self):
        return self._payroll_field_sum("salary")
    total_salary.short_description = "Salary"
    
    def total_cpp_deductions(self):
        return self._payroll_field_sum("cpp_deductions")
    total_cpp_deductions.short_description = "CPP"
    
    def total_ei_deductions(self):
        return self._payroll_field_sum("ei_deductions")
    total_ei_deductions.short_description = "EI"
    
    def total_provinical_deductions(self):
        return self._payroll_field_sum("provincial_tax_deductions")
    total_provinical_deductions.short_description = "Provinical"
    
    def total_federal_deductions(self):
        return self._payroll_field_sum("federal_tax_deductions")
    total_federal_deductions.short_description = "Federal"
        
    def total_deductions(self):
        return self._payroll_field_sum("total_deductions_on_income") 

    def total_net(self):
        return self._payroll_field_sum("net_amount")
    total_cpp_deductions.short_description = "Net"
        
        
"""
BC CLAIM CODES:
<select alt="<strong>Total claim amount from provincial TD1</strong>" class="sizable" name="claimCodeProv"><option value="0">Claim Code 0 (No claim amount)</option>
             <option selected="selected" value="1">Claim Code 1 (Minimum - 7,778.00)</option>
             <option value="2">Claim Code 2 (7,778.01 - 9,458.00)</option>
             <option value="3">Claim Code 3 (9,458.01 - 11,138.00)</option>
             <option value="4">Claim Code 4 (11,138.01 - 12,818.00)</option>
             <option value="5">Claim Code 5 (12,818.01 - 14,498.00)</option>
             <option value="6">Claim Code 6 (14,498.01 - 16,178.00)</option>
             <option value="7">Claim Code 7 (16,178.01 - 17,858.00)</option>
             <option value="8">Claim Code 8 (17,858.01 - 19,538.00)</option>
             <option value="9">Claim Code 9 (19,538.01 - 21,218.00)</option>
             <option value="10">Claim Code 10 (21,218.01 - 22,898.00)</option>
             <option value="11">Claim Code E (No tax)</option></select>

"""
