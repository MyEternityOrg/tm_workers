from datetime import datetime

from django import forms
from security.models import SecurityFact
from outsourcing.models import OutsourcingContractors, Enterprises


class SecurityForm(forms.ModelForm):

    class Meta:
        model = SecurityFact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SecurityForm, self).__init__(*args, **kwargs)
        self.fields['fact_hours'].widget.attrs['class'] = 'form-control'
