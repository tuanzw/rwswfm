from django import forms
from crispy_forms.helper import FormHelper

from ..models import Team, Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'active', 'team')

    team = forms.ModelChoiceField(
        queryset=Team.objects.none(),
        widget=forms.Select(
            attrs={'placeholder': 'Select Team'}
        )
    )
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # populate Team data
        self.fields['team'].queryset = Team.objects.filter(active=True)

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