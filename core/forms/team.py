from django import forms
from django.core.exceptions import ValidationError
from core.models import Team, Employee
from core.forms import BaseModelForm


class TeamForm(BaseModelForm):
    readonly_on_edit = ['name']

    # Explicitly declare the leader dropdown to filter for only ACTIVE employees
    leader = forms.ModelChoiceField(
        queryset=Employee.objects.filter(user__is_active=True).select_related('user'),
        required=False,
        label='Team Leader',
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="No Leader Assigned"
    )
    # Multi-select dropdown field for subteams management
    subteams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.filter(active=True),
        required=False,
        label='Assign Subteams',
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
    )
    class Meta:
        model = Team
        fields = ('name', 'leader', 'subteams', 'active',)
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Team',
                'class': 'form-control',
            }),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Team',
            'active': 'Is Active?',
        }
    def clean_subteams(self):
        subteams = self.cleaned_data.get('subteams')
        instance = self.instance

        if not subteams:
            return subteams

        # RULE 1: Protect against self-assignment anomalies
        if instance in subteams:
            raise ValidationError("A team cannot be designated as a subteam of itself.")

        # RULE 2: Defend against database recursion locks (Circular Dependencies)
        if instance.pk:
            # Gather any parent components assigning this precise record right now
            existing_parents = instance.parent_teams.all()
            
            for subteam in subteams:
                if subteam in existing_parents:
                    raise ValidationError(
                        f"Circular dependency block! '{subteam.name}' is already designated as a parent to this team."
                    )         
        return subteams
    
    def save(self, commit=True):
        instance: Team = super().save(commit=False)
        instance.name = instance.name.strip().upper()
        if commit:
            instance.save()
            self.save_m2m() # Save the Many-to-Many relationships (subteams) after the instance is saved
        return instance