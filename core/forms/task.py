# your_app/forms/task.py

from django import forms
from core.models import Task
from core.forms import BaseModelForm

class TaskForm(BaseModelForm):
    readonly_on_edit = ['name']  # name is visible but readonly in edit mode

    class Meta:
        model = Task
        fields = ('name', 'active')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Task',
                'class': 'form-control',
            }),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Task',
            'active': 'Is Active?',
        }

    def save(self, commit=True):
        instance: Task = super().save(commit=False)
        instance.name = instance.name.strip().upper()
        if commit:
            instance.save()
        return instance
