from django import forms
from django.forms import Form

from .models import Enterprises, ExtWorkerRecord


class CreateRecordForm(forms.ModelForm):
    guid = forms.CharField()
    person_name = forms.CharField()
    f_time = forms.TimeField()
    t_time = forms.TimeField()

    person_name.widget.attrs.update({'class': 'special', 'required': True, 'placeholder': "Введите ФИО сотрудника"})
    f_time.widget.attrs.update({'data-format': 'hh:mm', 'readonly': True, 'required': True})
    t_time.widget.attrs.update({'data-format': 'hh:mm', 'readonly': True, 'required': True})


    class Meta:
        model = ExtWorkerRecord
        exclude = ('dts',)

    def clean(self):
        cleaned_data = super().clean()
        f_time = cleaned_data.get("f_time")
        t_time = cleaned_data.get("t_time")

        if f_time > t_time :
            msg = "Время начала не может быть больше времени завершения!"
            self.add_error('f_time', msg)

    # def is_valid(self, *args, **kwargs):
    #     super(CreateRecordForm, self).__init__(*args, **kwargs)
    #     return True

class EditShopForm(Form):
    class Meta:
        model = ExtWorkerRecord
        fields = (
            'guid',
            'enterprise_guid',
            'dts',
            'person_name',
            'f_time',
            't_time',
            'duration'
        )

    def __init__(self, *args, **kwargs):
        super(EditShopForm, self).__init__(*args, **kwargs)


class FillShopDataForm(Form):
    class Meta:
        model = Enterprises
        fields = (
            'enterprise_code',
            'name'
        )

    def __init__(self, *args, **kwargs):
        super(FillShopDataForm, self).__init__(*args, **kwargs)
