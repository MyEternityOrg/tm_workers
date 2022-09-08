import selectors

import django_filters
from django_filters import *
from django_filters.widgets import *

from outsourcing.models import *


class PlanningStaffFilter(django_filters.FilterSet):
    contractor = ModelChoiceFilter(queryset=OutsourcingContractors.objects.filter(marked=0).order_by('name'),
                                   label='Контрагент', empty_label='--- Контрагент ---')
    enterprise = ModelChoiceFilter(queryset=Enterprises.get_list_shops(), label='Подразделение',
                                   empty_label='--- Подразделение ---')

    def __init__(self, *args, **kwargs):
        super(PlanningStaffFilter, self).__init__(*args, **kwargs)
        self.form.fields['contractor'].widget.attrs['class'] = 'form-select'
        self.form.fields['contractor'].widget.attrs['id'] = 'inputGroupSelect04'
        self.form.fields['contractor'].widget.attrs['selected'] = 'Контрагент'
        self.form.fields['enterprise'].widget.attrs['class'] = 'form-select'
        self.form.fields['enterprise'].widget.attrs['id'] = 'inputGroupSelect04'

    class Meta:
        model = OutsourcingPPlanning
        fields = ['contractor', 'enterprise']
        ordering = ['enterprise']


class PlanningPricesFilter(django_filters.FilterSet):
    contractor = ModelChoiceFilter(queryset=OutsourcingContractors.objects.filter(marked=0).order_by('name'),
                                   label='Контрагент', empty_label='--- Контрагент ---')
    enterprise = ModelChoiceFilter(queryset=Enterprises.get_list_shops(), label='Подразделение',
                                   empty_label='--- Подразделение ---')

    def __init__(self, *args, **kwargs):
        super(PlanningPricesFilter, self).__init__(*args, **kwargs)
        self.form.fields['contractor'].widget.attrs['class'] = 'form-select'
        self.form.fields['contractor'].widget.attrs['id'] = 'inputGroupSelect04'
        self.form.fields['contractor'].widget.attrs['selected'] = 'Контрагент'
        self.form.fields['enterprise'].widget.attrs['class'] = 'form-select'
        self.form.fields['enterprise'].widget.attrs['id'] = 'inputGroupSelect04'

    class Meta:
        model = OutsourcingPrices
        fields = ['contractor', 'enterprise']
        ordering = ['enterprise__name']