from django import forms
from django.forms import Form
from .models import Enterprises, ExtWorkerRecord


class EditShopForm(Form):
    class Meta:
        model = ExtWorkerRecord
        fields = (
            'guid',
            'enterprise_guid',
            'dts',
            'person_name',
            'person_birthd',
            'person_birthp]',
            'time_start',
            'time_stop',
            'duration',
            'contractor_name'
        )



class FillShopDataForm(Form):
    class Meta:
        model = Enterprises
        fields = ('enterprise_code', 'name')

    # def __init__(self, *args, **kwargs):
    #     super(FillShopDataForm, self).__init__(*args, **kwargs)
        # self.fields['first_name'].widget.attrs['placeholder'] = 'Иван'
        # self.fields['last_name'].widget.attrs['placeholder'] = 'Иванов'
        # self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        # self.fields['email'].widget.attrs['placeholder'] = 'myemail@mail.ml'
        # self.fields['password1'].widget.attrs['placeholder'] = 'Придумайте пароль'
        # self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        # for field_name, field in self.fields.items():
        #     field.widget.attrs['class'] = 'form-control py-4'


