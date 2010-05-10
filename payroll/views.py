from django.shortcuts import render_to_response
from django import forms

import django_filters

from payroll.models import Payroll


# TODO: Add easy date selection?
class DateRangeField(django_filters.fields.RangeField):
    # Django-Filter DateRangeFilter that really accepts a range of dates ;)
    def __init__(self, *args, **kwargs):
        fields = (
            forms.DateField(),
            forms.DateField(),
        )
        forms.MultiValueField.__init__(self, fields, *args, **kwargs)


class DateRangeFilter(django_filters.RangeFilter):
    field_class = DateRangeField


class PayrollFilterSet(django_filters.FilterSet):
    created_at = DateRangeFilter()
    
    class Meta:
        model = Payroll
        fields = ['created_at']


def payroll_list(request):
    qs = Payroll.objects.order_by("-created_at")
    f = PayrollFilterSet(request.GET, queryset=qs)
    ctx = {
        "filter": f,
    }    
    return render_to_response('payroll/payroll_list.html', ctx)