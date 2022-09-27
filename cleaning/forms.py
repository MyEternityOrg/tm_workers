from datetime import datetime

from django import forms
from cleaning.models import CleaningFact
from outsourcing.models import OutsourcingContractors, Enterprises


class CreateCleaningForm(forms.ModelForm):

    class Meta:
        model = CleaningFact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CreateCleaningForm, self).__init__(*args, **kwargs)
        self.fields['fact_hours'].widget.attrs['class'] = 'form-control'
