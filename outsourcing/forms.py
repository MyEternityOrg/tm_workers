import uuid
from datetime import datetime

from django import forms
from django.forms import DateInput, DateTimeInput

from outsourcing.models import OutsourcingPrices, OutsourcingContractors
from extworkers.models import Enterprises


# class UpdateRecordForm(forms.ModelForm):
#     guid = forms.CharField()
#     person_name = forms.CharField()
#     f_time = forms.TimeField()
#     t_time = forms.TimeField()
#     p_city = forms.CharField()
#     p_birthday = forms.DateField()
#     dts = forms.DateField()
#
#     guid.widget.attrs.update({'class': 'special', 'readonly': True})
#     person_name.widget.attrs.update({'class': 'special', 'required': True, 'placeholder': "Введите ФИО сотрудника"})
#     p_city.widget.attrs.update({'class': 'special', 'required': True, 'placeholder': "Место рождения сотрудника"})
#     f_time.widget.attrs.update({'data-format': 'hh:mm', 'readonly': True, 'required': True})
#     t_time.widget.attrs.update({'data-format': 'hh:mm', 'readonly': True, 'required': True})
#     p_birthday.widget.attrs.update({'data-format': 'yyyy-MM-dd', 'readonly': True, 'required': True})
#
#     class Meta:
#         model = ExtWorkerRecord
#         fields = '__all__'
#         # exclude = ('dts',)
#
#     def __init__(self, *args, **kwargs):
#         super(UpdateRecordForm, self).__init__(*args, **kwargs)
#         # self.fields['enterprise'].widget.attrs['visible'] = False
#
#     def clean(self):
#         cleaned_data = super().clean()
#         f_time = cleaned_data.get("f_time")
#         t_time = cleaned_data.get("t_time")
#
#         if f_time > t_time:
#             msg = "Время начала не может быть больше времени завершения!"
#             self.add_error('f_time', msg)


class CreatePriceForm(forms.ModelForm):
    guid = forms.CharField()
    contractor = forms.ModelChoiceField(OutsourcingContractors.objects.all().order_by('name'))
    enterprise = forms.ModelChoiceField(Enterprises.objects.filter(enterprise_code__gt=2).order_by('enterprise_code'))
    price = forms.FloatField()

    class Meta:
        model = OutsourcingPrices
        fields = '__all__'
        widgets = {
            'dts': (DateTimeInput(attrs={'type': 'datetime-local'}))
        }

    def __init__(self, *args, **kwargs):
        super(CreatePriceForm, self).__init__(*args, **kwargs)
        self.fields['dts'].widget.attrs['class'] = 'datetimepicker special'
        self.fields['dts'].widget.attrs['min'] = datetime.today().strftime("%Y-%m-%d %H:%M")
        self.fields['contractor'].widget.attrs['class'] = 'form-select'
        self.fields['enterprise'].widget.attrs['class'] = 'form-select'
        self.fields['contractor'].widget.attrs['required'] = True
        self.fields['enterprise'].widget.attrs['required'] = True
