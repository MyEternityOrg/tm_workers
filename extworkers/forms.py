from django.forms import Form
from django.views.generic import CreateView

from .models import Enterprises, ExtWorkerRecord


class CreatePersonForm(CreateView):
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


class FillShopDataForm(Form):
    class Meta:
        model = Enterprises
        fields = (
            'enterprise_code',
            'name'
        )
