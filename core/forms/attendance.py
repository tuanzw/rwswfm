from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper

from ..models import Attendance, Employee

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('empid', 'date', 'site_id', 'sys_intime', 'sys_outtime', 'sup_intime', 'sup_outtime', 'workday', 'ot', 'ot_night', 'approved', 'dayoff')

    empid = forms.ModelChoiceField(
        queryset=Employee.objects.none(),
        widget=forms.Select(
            attrs={'placeholder': 'Select Employee'}
        )
    )
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                   'min': timezone.now().date(),
                   'type': 'date',
                   }
        )
    )
    sys_intime = forms.TimeField(
        input_formats=['%I:%M'],
        label='System InTime',
        widget=forms.TimeInput(
            attrs={'type': 'time',},
        )
    )
    sys_outtime = forms.TimeField(
        label='System OutTime',
        widget=forms.TimeInput(
            attrs={'type': 'time',},
        )
    )
    sup_intime = forms.TimeField(
        label='Sup Confirmed InTime',
        required=False,
        widget=forms.TimeInput(
            attrs={'type': 'time',}, 
        )
    )
    sup_outtime = forms.TimeField(
        label='Sup Confirmed OutTime',
        required=False,
        widget=forms.TimeInput(
            attrs={'type': 'time',}
        )
    )
    workday = forms.DecimalField(required=False)
    ot = forms.IntegerField(required=False)
    ot_night = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # populate Employee data
        self.fields['empid'].queryset = Employee.objects.filter(active=True)

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
            _start = timezone.datetime.combine(instance.date, instance.sys_intime)
            _end = timezone.datetime.combine(instance.date, instance.sys_outtime)
            instance.duration = _end - _start
            hours, _ = divmod(instance.duration.total_seconds(), 3600)
            if hours >=3 and hours < 5:
                instance.workday = 0.5
            elif hours >= 5:
                instance.workday = 1.0
            else:
                instance.workday = 0.0
        else: # edit mode
            pass
        if commit:
            instance.save()
        return instance