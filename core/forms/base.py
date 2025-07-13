# your_app/forms/base.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class BaseModelForm(forms.ModelForm):
    # List of field names to be made readonly on edit
    readonly_on_edit = []
    disabled_on_edit = []
    fields_to_hide = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        is_edit_mode = self.instance and self.instance.pk

        # Prioritize hiding
        for field_name in self.fields_to_hide:
            if field_name in self.fields:
                self.fields[field_name].widget = forms.HiddenInput()

        # Only apply readonly/disabled if not hidden
        for field_name in self.readonly_on_edit:
            if field_name in self.fields and is_edit_mode and field_name not in self.fields_to_hide:
                self.fields[field_name].widget.attrs['readonly'] = True

        for field_name in self.disabled_on_edit:
            if field_name in self.fields and is_edit_mode and field_name not in self.fields_to_hide:
                self.fields[field_name].widget.attrs['disabled'] = True

        # Setup crispy helper
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(*(Field(f) for f in self.fields if f not in self.fields_to_hide))
