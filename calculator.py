import pprint
import string

from lxml import html as HTML
from mechanize import Browser


ENDPOINT = "https://apps.cra-arc.gc.ca/ebci/rhpd/startLanguage.do?lang=English"


class PayrollCalculator(object):
    """
    Calculate's payroll taxes from the CRA online payroll calculator.
    
    """
    def __init__(self, salary, cpp_to_date, ei_to_date, ei_exempt, payperiod):
        self.payperiod = str(payperiod)
        self.salary = str(salary)
        self.cpp_to_date = str(cpp_to_date)
        self.ei_to_date = str(ei_to_date)
        self.ei_exempt = ei_exempt
        
        # Setup the Mechanize Browser.
        self.b = Browser()
        self.b.set_handle_robots(False)
        self.b.open(ENDPOINT)
        

    def calculate(self):
        # https://apps.cra-arc.gc.ca/ebci/rhpd/startLanguage.do?lang=English
    
        # 1. Enter Pay Period information.
        print "PAY"
        print self.b.geturl()
        self.b.select_form(name="welcomeData")
        # January 1, 2010 - "7"
        # January 1, 2009 - "4"
        self.b.form["year"] = ["7"]
        # British Columbia - "9"
        self.b.form["province"] = ["9"]
        # Biweekly - "2"
        # Monthly - "4"
        self.b.form["payPeriod"] = [self.payperiod]
        self.b.submit(name="fwdSalary")

        # 2. Salary, Bonus Etc.
        print "SALARY"
        print self.b.geturl()
        self.b.select_form(name="payrollData")
        self.b.form["yearToDateCPPAmount"] = self.cpp_to_date
        
        if self.ei_exempt:
            # EI exempt - "2"
            self.b.form["yearToDateEI"] = ["2"]
        else:
            self.b.form["yearToDateEIAmount"] = self.ei_to_date
        
        self.b.submit(name="fwdGrossSalary")

        # 3. Gross Income
        print "GROSS"
        print self.b.geturl()
        self.b.select_form(name="grossIncomeData")
        self.b.form["incomeTypeAmount"] = self.salary
        self.b.submit()

        # 4. Salary / Bonus Etc. again
        print "SALARY"
        print self.b.geturl()
        self.b.select_form(name="payrollData")
        # We need to press the "Calculate" button - it's number 3!
        self.b.submit(nr=3)
        
        # 5. Results page. Scraping time!
        self.doc = HTML.fromstring(self.b.response().read(), self.b.geturl())
        return self._needle()    
    
    def _needle(self):
        # The data we want is trapped somewhere around here.
        fields = [
            "Salary or wages for the pay period",
            "Total EI insurable earnings for the pay period",
            "Taxable income",
            "Cash income for the pay period",
            "Federal tax deductions",
            "Provincial tax deductions",
            "Requested additional tax deduction",
            "Total tax on income",
            "CPP deductions",
            "EI deductions",
            "Amounts deducted at source",
            "Total deductions on income",
            "Net amount"
        ]
        
        # .width50 would also work ;)
        values = [string2dollar(td.text) for td in self.doc.xpath("//table[3]//td[2]")]
        values.append(string2dollar(self.doc.xpath("//table[4]//td[2]")[0].text))
        
        print string2dollar(self.doc.xpath("//table[4]//td[2]")[0].text)
        
        pprint.pprint(zip(fields, values))
        
        return values
        #return zip(fields, values)


def string2dollar(s):
    return round(float(''.join(c for c in s if c in string.digits + '.')), 2)