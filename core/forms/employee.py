from datetime import datetime

from django import forms
from django.db import transaction
from django.contrib.auth.models import Group
from core.models import Employee, User
from core.forms import BaseModelForm
from core.models.team import Team

class EmployeeForm(BaseModelForm):
    employee_code = forms.CharField(
        max_length=20,
        required=True,
        label='Employee Code',
        widget=forms.TextInput(attrs={
            'placeholder': 'Employee Code', 'class': 'form-control', 'style': 'text-transform: uppercase;',}),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: capitalize;',}),
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: capitalize;',}),
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.filter(active=True),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False,
        label='Assigned Teams'
    )
    active = forms.BooleanField(
        required=False,
        label='Is Active',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    # Add the Role selection field directly to the form
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label='Role',
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Standard Employee (No Special Role)"
    )
    readonly_on_edit = ['employee_code']  # employee_code is visible but readonly in edit mode

    field_order = [
        'employee_code', 
        'first_name', 
        'last_name', 
        'gender', 
        'dob', 
        'id_number', 
        'teams', 
        'active',
        'role',
    ]

    class Meta:
        model = Employee
        fields = ('gender', 'dob', 'id_number', 'teams',)
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'dob': forms.DateInput(attrs={
                'placeholder': 'Date of Birth', 'class': 'form-control', 'type': 'date',}),
            'id_number': forms.TextInput(attrs={
                'placeholder': 'ID Number', 'class': 'form-control',}),
        }

        # help_texts = {
        #     'code': 'Unique employee code (will be converted to uppercase)',
        #     'id_number': 'Numeric ID only',
        #     'dob': 'Date of Birth',
        # }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Capture the user from kwargs
        super().__init__(*args, **kwargs)
        # Prepopulate User related fields from the linked User instance if we are editing
        if self.instance and self.instance.pk and hasattr(self.instance, 'user'):
            self.fields['employee_code'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['active'].initial = self.instance.user.is_active

            # Fetch their first group role
            current_role = self.instance.user.groups.first()
            if current_role:
                self.fields['role'].initial = current_role.id

    def clean_employee_code(self):
        """Validate unique constraint for username in the User model during creation."""
        code = self.cleaned_data['employee_code'].strip().upper()
        
        if not self.instance.pk:
            if User.objects.filter(username=code).exists():
                raise forms.ValidationError("An employee with this code/username already exists.")
        return code

    def save(self, commit=True):
        with transaction.atomic():
            instance: Employee = super().save(commit=False)
            code = self.cleaned_data['employee_code']
            f_name = self.cleaned_data['first_name'].strip().title()
            l_name = self.cleaned_data['last_name'].strip().title()
            is_active_status = self.cleaned_data.get('active', True)
            operator_username = self.user.username if self.user else 'system'

            selected_role = self.cleaned_data.get('role')

            if not instance.pk:
                # STEP 1: Create the User account using employee_code as username
                current_year = datetime.now().year
                default_password = f"{code.capitalize()}@{current_year}"
                new_user = User.objects.create_user(
                    username=code,
                    password=default_password,
                    is_active=is_active_status,
                    first_name=f_name,
                    last_name=l_name
                )
                # STEP 2: Associate employee with the newly created user
                instance.user = new_user
                instance.created_by = operator_username
            else:
                # If editing, sync the active flag with the User record & update audit trailing
                instance.updated_by = operator_username
                instance.user.is_active = is_active_status
                instance.user.first_name = f_name
                instance.user.last_name = l_name
                instance.user.save()

            # Handle Role Syncing
            if selected_role:
                # Clear old groups and set the single new group role cleanly
                instance.user.groups.set([selected_role])
            else:
                instance.user.groups.clear()

            # Capitalize and save the names to the User model
            instance.user.first_name = f_name
            instance.user.last_name = l_name

            if commit:
                instance.save()
                self.save_m2m()  # Saves 'teams' relationships safely
        return instance