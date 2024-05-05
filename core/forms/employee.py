from django import forms
from crispy_forms.helper import FormHelper

from ..models import Vendor, Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('empid', 'name', 'pin', 'active', 'vendor')

    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.none(),
        widget=forms.Select(
            attrs={'placeholder': 'Select Vendor'}
        )
    )
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # populate Vendor data
        self.fields['vendor'].queryset = Vendor.objects.filter(active=True)

        instance = getattr(self, 'instance', None)
        # edit mode
        if instance and instance.pk:
            # disable name
            self.fields['empid'].disabled = True
        
        # Enable crispy form
        self.helper = FormHelper(self)
        # Don't generate Form tag
        self.helper.form_tag = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        # model_instance._state.adding is True meaning update mode
        if instance._state.adding:
            pass
        else: # edit mode
            pass
        if commit:
            instance.save()
        return instance