from datetime import datetime

from django import forms
from django.forms import DateTimeInput

from extworkers.models import Enterprises
from outsourcing.models import OutsourcingPrices, OutsourcingContractors, OutsourcingPPlanning


class CreatePriceForm(forms.ModelForm):
    guid = forms.CharField()
    contractor = forms.ModelChoiceField(OutsourcingContractors.objects.all().order_by('name'))
    enterprise = forms.ModelChoiceField(Enterprises.get_list_shops().order_by('enterprise_code'))
    price = forms.FloatField()

    class Meta:
        model = OutsourcingPrices
        fields = '__all__'
        widgets = {
            'dts': (DateTimeInput(attrs={'type': 'datetime-local'}))
        }

    def __init__(self, *args, **kwargs):
        super(CreatePriceForm, self).__init__(*args, **kwargs)
        self.fields['dts'].widget.attrs['class'] = 'datetimepicker form-control'
        self.fields['dts'].widget.attrs['min'] = datetime.today().strftime("%Y-%m-%d %H:%M")
        self.fields['contractor'].widget.attrs['class'] = 'form-select'
        self.fields['enterprise'].widget.attrs['class'] = 'form-select'
        self.fields['contractor'].widget.attrs['required'] = True
        self.fields['enterprise'].widget.attrs['required'] = True
        self.fields['price'].widget.attrs['class'] = 'form-control'


class CreatePlanningRecordForm(forms.ModelForm):
    guid = forms.CharField()
    contractor = forms.ModelChoiceField(OutsourcingContractors.objects.all().order_by('name'))
    enterprise = forms.ModelChoiceField(
        Enterprises.get_list_shops().order_by('enterprise_code'))
    amount = forms.IntegerField()

    class Meta:
        model = OutsourcingPPlanning
        fields = '__all__'
        widgets = {
            'dts': (DateTimeInput(attrs={'type': 'datetime-local'}))
        }

    def __init__(self, *args, **kwargs):
        super(CreatePlanningRecordForm, self).__init__(*args, **kwargs)
        self.fields['dts'].widget.attrs['class'] = 'datetimepicker form-control'
        self.fields['dts'].widget.attrs['min'] = datetime.today().strftime("%Y-%m-%d %H:%M")
        self.fields['contractor'].widget.attrs['class'] = 'form-select'
        self.fields['enterprise'].widget.attrs['class'] = 'form-select'
        self.fields['contractor'].widget.attrs['required'] = True
        self.fields['enterprise'].widget.attrs['required'] = True
        self.fields['amount'].widget.attrs['class'] = 'form-control'
        self.fields['gender'].widget.attrs['class'] = 'form-select'
