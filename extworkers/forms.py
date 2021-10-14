from django import forms
from django.forms import Form, CharField, Textarea

from .models import Enterprises, ExtWorkerRecord


class CreateRecordForm(forms.ModelForm):
    person_name = CharField(help_text='TEST')

    class Meta:
        model = ExtWorkerRecord
        exclude = ('dts',)
        widgets = {
            'person_name': Textarea(attrs={'cols': 80, 'rows': 20}),
        }


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
