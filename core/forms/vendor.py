from django import forms
from crispy_forms.helper import FormHelper

from ..models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('name', 'active',)


    name = forms.CharField(max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Vendor name'
        }))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        # edit mode
        if instance and instance.pk:
            # disable name
            self.fields['name'].disabled = True
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