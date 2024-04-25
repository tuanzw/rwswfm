from django import forms
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper

from ..models import Carrier
from ..validators import alphanumeric


class CarrierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['carrier'].disabled = True
            
        self.helper = FormHelper(self)
        self.helper.form_tag = False
    
    class Meta:
        model = Carrier
        fields = ('carrier', 'name', 'address')
        widgets = {
            'carrier': forms.TextInput(attrs={
                'length': 20,
                'placeholder': 'Only alphaNumeric accepted!',
                'hx-get': reverse_lazy('check_carrier'),
                'hx-trigger': 'keyup changed delay:500ms',
                'hx-target': '#div_id_carrier',
                'hx-swap': 'outerHTML',
            }),
            'name': forms.TextInput(attrs={
                'length': 200,
                'placeholder': 'Name'
            }),
            'address': forms.TextInput(attrs={
                'length': 300,
                'placeholder': 'Address'
            }),
        }
    
    def clean_carrier(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.carrier
        else:
            inputted_carrier = self.cleaned_data['carrier']
            alphanumeric(inputted_carrier)
            return inputted_carrier
        
        
    def save(self, commit=True):
        carrier = super().save(commit=False)
        if commit:
            carrier.save()
        return carrier