import datetime
import uuid
from datetime import datetime

from django import forms
from django.forms import Form, Textarea

from .models import Enterprises, ExtWorkerRecord


class CreateRecordForm(forms.ModelForm):
    guid = forms.CharField()
    person_name = forms.CharField()
    enterprise = forms.CharField()
    dts = forms.DateField()
    f_time = forms.TimeField()
    t_time = forms.TimeField()

    person_name.widget.attrs.update({'class': 'special'})
    f_time.widget.attrs.update({'data-format': 'hh:mm', 'readonly': False, 'required': True})
    t_time.widget.attrs.update({'data-format': 'hh:mm', 'readonly': False, 'required': True})

    class Meta:
        model = ExtWorkerRecord
        exclude = ('dts',)

    # def __init__(self, *args, **kwargs):
    #     super(CreateRecordForm, self).__init__(*args, **kwargs)
    #     self.instance.enterprise = Enterprises.objects.get(guid='0940D36F-845E-11E1-B5AB-002264F5ABA4')


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
