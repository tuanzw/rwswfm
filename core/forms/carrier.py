from django import forms
from django.urls import reverse_lazy


from core.models import Carrier
from core.forms import BaseModelForm
from core.validators import alphanumeric


class CarrierForm(BaseModelForm):
    readonly_on_edit = ['carrier']
    
    class Meta:
        model = Carrier
        fields = ('carrier', 'name', 'active', 'address')
        widgets = {
            'carrier': forms.TextInput(attrs={
                'length': 30,
                'placeholder': 'Carrier - Only Alphanumeric & hyphen',
                'hx-get': reverse_lazy('check_carrier'),
                'hx-trigger': 'keyup changed delay:500ms',
                'hx-target': '#div_id_carrier', # div_id_carrier created by crispy
                'hx-swap': 'outerHTML',
            }),
            'name': forms.TextInput(attrs={
                'length': 200,
                'placeholder': 'Name',
                'class': 'form-control',
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'address': forms.TextInput(attrs={
                'length': 300,
                'placeholder': 'Address',
                'class': 'form-control',
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
        instance: Carrier = super().save(commit=False)
        instance.carrier = instance.carrier.strip().upper()
        if commit:
            instance.save()
        return instance