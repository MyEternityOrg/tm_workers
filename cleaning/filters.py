import datetime
import calendar

import django_filters
from django.forms import DateInput
from django_filters import *

from cleaning.models import *


class CleaningFilter(django_filters.FilterSet):
    dts = DateFilter(widget=DateInput(attrs={'type': 'month'}))
    enterprise = ModelChoiceFilter(queryset=Enterprises.get_list_shops(), label='Подразделение',
                                   empty_label='--- Подразделение ---')

    def __init__(self, *args, **kwargs):
        super(CleaningFilter, self).__init__(*args, **kwargs)

        self.form.fields['enterprise'].widget.attrs['class'] = 'form-select'
        self.form.fields['enterprise'].widget.attrs['id'] = 'inputGroupSelect04'

        # self.form.fields['dts'].widget.attrs['class'] = 'form-control'
        # # self.form.fields['dts'].widget.attrs['class'] = 'datetimepicker'

    def filter_queryset(self, queryset):

        qs = queryset
        dts = self.data.get('dts')
        if dts:
            f_year = int(dts[:4])
            f_month = int(dts[5:7])
            today = datetime.date.today()
            if today.month == f_month and today.year == f_year:
                end_day = today.day
            else:
                interval_month = calendar.monthrange(f_year, f_month)
                end_day = interval_month[1]

            qs = queryset.filter(dts__gte=datetime.date(f_year, f_month, 1),
                                      dts__lte=datetime.date(f_year, f_month, end_day))

        ent = self.data.get('enterprise')
        if ent:
            qs = qs.filter(enterprise=ent)

        return qs

    class Meta:
        model = CleaningPlan
        fields = ['dts', 'enterprise']
        ordering = ['enterprise__name']
