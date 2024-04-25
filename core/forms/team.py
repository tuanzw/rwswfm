from django import forms
from crispy_forms.helper import FormHelper

from ..models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'active',)


    name = forms.CharField(max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Team name'
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
        team = super().save(commit=False)
        if commit:
            team.save()
        return team