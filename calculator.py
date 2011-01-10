import datetime
import pprint
import string

from lxml import html as HTML
from mechanize import Browser


ENDPOINT = 'https://apps.cra-arc.gc.ca/ebci/rhpd/startLanguage.do?lang=English'


def string2dollar(s):
    return round(float(''.join(c for c in s if c in string.digits + '.')), 2)

# payroll(4000, 0, 0, False, '2')
def payroll(salary, cpp_to_date, ei_to_date, ei_exempt, payperiod):    
    # We'll need the date later.
    year, month, day = datetime.datetime.now().strftime('%Y %m %d').split(' ')
    
    # Setup Mechanize Browser.
    b = Browser()
    b.set_handle_robots(False)
    b.open(ENDPOINT)
    
    print 'STEP 0 - SETUP'
    print ENDPOINT
    
    b.select_form(nr=0)
    b.form['calculationType'] = ['salary']
    b.submit('goStep1')
    
    print 'STEP 1 - INFO'
    print b.geturl()
    
    b.select_form(nr=0)
    # British Columbia
    b.form['province'] = ['9']
    # Pay Period
    # Bi-weekly - '2'
    # Monthly - '4'
    # b.form['payPeriod'] = ['4']
    b.form['payPeriod'] = [payperiod]
    # Date the employee is paid
    # 2010
    # 01
    # 01
    b.form['cmbFirstYear'] = [year]
    b.form['cmbFirstMonth'] = [month]
    b.form['cmbFirstDay'] = [day]
    b.submit('goStep2AddOption')
    
    print 'STEP 2 - INCOME'
    print b.geturl()
    
    b.select_form(nr=0)
    # b.form['incomeTypeAmount'] = '4000'
    b.form['incomeTypeAmount'] = str(salary)
    b.submit('goStep2Option')
    
    print 'STEP 3 - SALARY'
    print b.geturl()
    
    b.select_form(nr=0)
    # CPP
    b.form['yearToDateCPPAmount'] = str(cpp_to_date)
    # EI
    # EI exempt - '2'
    if ei_exempt:
        b.form['yearToDateEI'] = ['2']
    else:
        b.form['yearToDateEIAmount'] = str(ei_to_date)
    b.submit('goResults')
    
    print 'STEP 4 - GOODS'
    print b.geturl()
    
    doc = HTML.fromstring(b.response().read(), b.geturl())
    fields = {
        'salary': '//*[@class="table"]/ul[3]/li[1]',
        'cash_income': '//*[@class="table"]/ul[4]/li[2]/strong',
        'taxable_income': '//*[@class="table"]/ul[3]/li[4]',
        # 'Pensionable earnings for the pay period': '//*[@class="table"]/ul[3]/li[5]',
        'ei_insurable_earnings': '//*[@class="table"]/ul[3]/li[6]',
        'federal_tax_deductions': '//*[@class="table"]/ul[2]/li[7]',
        'provincial_tax_deductions': '//*[@class="table"]/ul[2]/li[8]',
        'additional_tax_deductions': '//*[@class="table"]/ul[2]/li[9]',
        'total_tax_on_income': '//*[@class="table"]/ul[3]/li[10]',
        'cpp_deductions': '//*[@class="table"]/ul[3]/li[11]',
        'ei_deductions': '//*[@class="table"]/ul[3]/li[12]',
        'amounts_deducted_at_source': '//*[@class="table"]/ul[3]/li[13]',
        'total_deductions_on_income': '//*[@class="table"]/ul[4]/li[14]/strong',
        'net_amount': '//*[@class="table"]/ul[4]/li[15]/strong'
    }
    
    values = {}
    for name, xpath in fields.items():
        values[name] = string2dollar(doc.xpath(xpath)[0].text)
        
    import pprint
    pprint.pprint(values)
        
    return values