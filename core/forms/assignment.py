from django import forms
from crispy_forms.helper import FormHelper
from django.utils.timezone import now

from ..models import Task, Assignment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('empid', 'task', 'rfid', 'buff', 'listid', 'status', 'estimate_mi')
    

    def __init__(self, *args, **kwargs):
        # get login user passed through from view
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        # populate Team data
        self.fields['task'].queryset = Task.objects.filter(active=True)
        
        # Enable crispy form
        self.helper = FormHelper(self)
        # Don't generate Form tag
        self.helper.form_tag = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        # model_instance._state.adding is False meaning update mode
        if not instance._state.adding:
            instance.updatedby = self.user.username
            instance.updatedat = now()
        else: # model_instance._state.adding is True meaning create mode
            instance.createdby = self.user.username
        if commit:
            instance.save()
        return instance