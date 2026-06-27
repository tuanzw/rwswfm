from django import forms
from core.models import Employee
from core.forms import BaseModelForm
from core.models.team import Team

class EmployeeForm(BaseModelForm):
    readonly_on_edit = ['code']  # code is visible but readonly in edit mode
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.filter(active=True),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False,
        label='Assigned Teams'
    )

    class Meta:
        model = Employee
        fields = ('code', 'name', 'gender', 'dob', 'id_number', 'active', 'teams',)
        widgets = {
            'code': forms.TextInput(attrs={
                'placeholder': 'Employee Code', 'class': 'form-control', 'style': 'text-transform: uppercase;',}),
            'name': forms.TextInput(attrs={
                'placeholder': 'Employee Name', 'class': 'form-control', 'style': 'text-transform: capitalize;',}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'dob': forms.DateInput(attrs={
                'placeholder': 'Date of Birth', 'class': 'form-control', 'type': 'date',}),
            'id_number': forms.TextInput(attrs={
                'placeholder': 'ID Number', 'class': 'form-control',}),
            'active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',}),
            'teams': forms.SelectMultiple(attrs={
                'class': 'form-control',}),
        }

        # help_texts = {
        #     'code': 'Unique employee code (will be converted to uppercase)',
        #     'id_number': 'Numeric ID only',
        #     'dob': 'Date of Birth',
        # }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Capture the user from kwargs
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance: Employee = super().save(commit=False)
        instance.code = instance.code.strip().upper()
        if not instance.pk:
            instance.created_by = self.user.username if self.user else 'system'
        else:
            instance.updated_by = self.user.username if self.user else 'system'
        if commit:
            instance.save()
            self.save_m2m()  # Save the many-to-many data for the form.
        return instance